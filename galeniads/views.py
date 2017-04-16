from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = 'galeniads/login.html'
    return render(request, template)
