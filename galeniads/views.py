from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
from .models import *

# Create your views here.
def index(request):
    template = 'galeniads/login.html'
    if request.method == 'POST':
        return redirect('home/')
    return render(request, template)

def home(request):
    template = 'galeniads/home.html'
    return render(request, template)

def register(request):
    #Still Dummy
    template = 'galeniads/register.html'
    return render(request, template)

def login(request):
    template ='galeniads/login.html'
    if request.method == 'POST':
        return redirect('home/')
    return render(request, template)
