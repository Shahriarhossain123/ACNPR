from django import forms
from .models import Car, Driver


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['plate_photo']


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'phone', 'address', 'car', 'photo', 'entry_time']
