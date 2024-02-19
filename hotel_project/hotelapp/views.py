from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    g = 'hello'
    return render(request, 'index.html')


def amenities(request):
    return render(request, 'amenities.html')


def contact(request):
    return render(request, 'contact.html')


def booking(request):
    return render(request, 'booking.html')


def login(request):
    return render(request, 'login.html')


def room(request):
    return render(request, 'room.html')


def about(request):
    return render(request, 'about.html')
