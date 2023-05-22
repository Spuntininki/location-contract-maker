from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return HttpResponse('<h1>Olá mundo! esse é o meu novo site.</h1>')
