from django.http import HttpResponse
from django.shortcuts import render
from serfa_panel.models import measurement, Sensor, Unit
import datetime

def helloo(request):
    return HttpResponse("Hello world")

def add_mes(request):
    if 'mad' in request.GET and request.GET['mad']:
        key = request.GET['key']
        value = request.GET['value']
        unit = request.GET['unit']
        m = measurement(sensor=Sensor.objects.get(key=key), date=datetime.datetime.now(), value=value, unit=Unit.objects.get(name=unit))
        m.save()

    else:
        return HttpResponse('Something went wrong.')