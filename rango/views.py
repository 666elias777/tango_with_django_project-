from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("<p>Rango says hey there partner!</p><p><a href='/rango/about/'>About</a>")

def about(request):
    return HttpResponse("<p>Rango says here is the about page.</p><p><a href='/rango/'>Index</a>")
