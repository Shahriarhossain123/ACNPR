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
