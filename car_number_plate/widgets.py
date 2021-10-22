import json
from datetime import date, datetime
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import datetime_safe, timezone
from django.utils.dateparse import parse_duration
from django.utils.encoding import force_str, smart_str


class Widget:
    def clean(self, value, row=None, *args, **kwargs):
        return value

    def render(self, value, obj=None):
        return force_str(value)


class NumberWidget(Widget):
    def is_empty(self, value):
        if isinstance(value, str):
            value = value.strip()
        # 0 is not empty
        return value is None or value == ""

    def render(self, value, obj=None):
        return value


class FloatWidget(NumberWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if self.is_empty(value):
            return None
        return float(value)


class IntegerWidget(NumberWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if self.is_empty(value):
            return None
        return int(float(value))


class DecimalWidget(NumberWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if self.is_empty(value):
            return None
        return Decimal(force_str(value))


class CharWidget(Widget):
    def render(self, value, obj=None):
        return force_str(value)


class BooleanWidget(Widget):

    TRUE_VALUES = ["1", 1, True, "true", "TRUE", "True"]
    FALSE_VALUES = ["0", 0, False, "false", "FALSE", "False"]
    NULL_VALUES = ["", None, "null", "NULL", "none", "NONE", "None"]

    def render(self, value, obj=None):
        if value in self.NULL_VALUES:
            return ""
        return self.TRUE_VALUES[0] if value else self.FALSE_VALUES[0]

    def clean(self, value, row=None, *args, **kwargs):
        if value in self.NULL_VALUES:
            return None
        return True if value in self.TRUE_VALUES else False


class DateWidget(Widget):
    def __init__(self, format=None):
        if format is None:
            if not settings.DATE_INPUT_FORMATS:
                formats = ("%Y-%m-%d",)
            else:
                formats = settings.DATE_INPUT_FORMATS
        else:
            formats = (format,)
        self.formats = formats

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        if isinstance(value, date):
            return value
        for format in self.formats:
            try:
                return datetime.strptime(value, format).date()
            except (ValueError, TypeError):
                continue
        raise ValueError("Enter a valid date.")

    def render(self, value, obj=None):
        if not value:
            return ""
        try:
            return value.strftime(self.formats[0])
        except:
            return datetime_safe.new_date(value).strftime(self.formats[0])


class DateTimeWidget(Widget):
    def __init__(self, format=None):
        if format is None:
            if not settings.DATETIME_INPUT_FORMATS:
                formats = ("%Y-%m-%d %H:%M:%S",)
            else:
                formats = settings.DATETIME_INPUT_FORMATS
        else:
            formats = (format,)
        self.formats = formats

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        for format in self.formats:
            try:
                dt = datetime.strptime(value, format)
                if settings.USE_TZ:
                    # make datetime timezone aware so we don't compare
                    # naive datetime to an aware one
                    dt = timezone.make_aware(dt,
                                             timezone.get_default_timezone())
                return dt
            except (ValueError, TypeError):
                continue
        raise ValueError("Enter a valid date/time.")

    def render(self, value, obj=None):
        if not value:
            return ""
        if settings.USE_TZ:
            value = timezone.localtime(value)
        return value.strftime(self.formats[0])


class TimeWidget(Widget):
    def __init__(self, format=None):
        if format is None:
            if not settings.TIME_INPUT_FORMATS:
                formats = ("%H:%M:%S",)
            else:
                formats = settings.TIME_INPUT_FORMATS
        else:
            formats = (format,)
        self.formats = formats

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        for format in self.formats:
            try:
                return datetime.strptime(value, format).time()
            except (ValueError, TypeError):
                continue
        raise ValueError("Enter a valid time.")

    def render(self, value, obj=None):
        if not value:
            return ""
        return value.strftime(self.formats[0])


class DurationWidget(Widget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None

        try:
            return parse_duration(value)
        except (ValueError, TypeError):
            raise ValueError("Enter a valid duration.")

    def render(self, value, obj=None):
        if value is None:
            return ""
        return str(value)


class SimpleArrayWidget(Widget):
    def __init__(self, separator=None):
        if separator is None:
            separator = ','
        self.separator = separator
        super().__init__()

    def clean(self, value, row=None, *args, **kwargs):
        return value.split(self.separator) if value else []

    def render(self, value, obj=None):
        return self.separator.join(str(v) for v in value)


class JSONWidget(Widget):
    def clean(self, value, row=None, *args, **kwargs):
        val = super().clean(value)
        if val:
            try:
                return json.loads(val)
            except json.decoder.JSONDecodeError:
                return json.loads(val.replace("'", "\""))

    def render(self, value, obj=None):
        if value:
            return json.dumps(value)


class ForeignKeyWidget(Widget):
    def __init__(self, model, field='pk', *args, **kwargs):
        self.model = model
        self.field = field
        super().__init__(*args, **kwargs)

    def get_queryset(self, value, row, *args, **kwargs):
        return self.model.objects.all()

    def clean(self, value, row=None, *args, **kwargs):
        val = super().clean(value)
        if val:
            return self.get_queryset(value, row, *args, **kwargs).get(**{self.field: val})
        else:
            return None

    def render(self, value, obj=None):
        if value is None:
            return ""

        attrs = self.field.split('__')
        for attr in attrs:
            try:
                value = getattr(value, attr, None)
            except (ValueError, ObjectDoesNotExist):
                # needs to have a primary key value before a many-to-many
                # relationship can be used.
                return None
            if value is None:
                return None

        return value


class ManyToManyWidget(Widget):
    def __init__(self, model, separator=None, field=None, *args, **kwargs):
        if separator is None:
            separator = ','
        if field is None:
            field = 'pk'
        self.model = model
        self.separator = separator
        self.field = field
        super().__init__(*args, **kwargs)

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return self.model.objects.none()
        if isinstance(value, (float, int)):
            ids = [int(value)]
        else:
            ids = value.split(self.separator)
            ids = filter(None, [i.strip() for i in ids])
        return self.model.objects.filter(**{
            '%s__in' % self.field: ids
        })

    def render(self, value, obj=None):
        ids = [smart_str(getattr(obj, self.field)) for obj in value.all()]
        return self.separator.join(ids)
