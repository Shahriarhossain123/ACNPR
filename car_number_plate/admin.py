from django.contrib import admin
from .models import Car, Driver


# Register your models here.
class CarAdmin(admin.ModelAdmin):
    list_display = ('number_plate', 'entry_time', 'entry_time')


class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'car', 'entry_time')


admin.site.register(Car)
admin.site.register(Driver)
