from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def landing(request):
    return render(request, template_name='index.html')


def equipo(request):
    return render(request, template_name='equipo.html')

def herramientas(request):
    return render(request, template_name='herramientas.html')
