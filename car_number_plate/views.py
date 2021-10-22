from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Car, Driver
from .forms import CarForm, DriverForm


# Create your views here.
def index(request):
    car_list = Car.objects.all()
    context = {
        'car_list': car_list,
    }
    return render(request, 'car/index.html', context)


class IndexClassView(ListView):
    model = Car
    template_name = 'car/index.html'
    context_object_name = 'car_list'


def car_driver(request):
    driver_list = Driver.objects.all()
    context = {
        'driver_list': driver_list,
    }
    return render(request, 'car/car_driver.html', context)


class Car_DriverClassView(ListView):
    model = Driver
    template_name = 'car/car_driver.html'
    context_object_name = 'driver_list'


def report(request):
    driver_list = Driver.objects.all()
    context = {
        'driver_list': driver_list,
    }
    return render(request, 'car/report.html', context)


class ReportClassView(ListView):
    model = Driver
    template_name = 'car/report.html'
    context_object_name = 'driver_list'
