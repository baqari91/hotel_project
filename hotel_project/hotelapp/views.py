from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Room


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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Email or password you entered is incorrect. '
                                   'Please check your credentials and try again.')
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def profile(request):
    return render(request, 'profile.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']

        if password == repeat_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'An account with this email already exists.')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'An account with this username already exists.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Unfortunately, the passwords you provided don't match. Kindly "
                                   "double-check and enter the same password in both fields.")
            return redirect('register')
    else:
        return render(request, 'register.html')


# room function to display the rooms
def room(request):
    rooms = Room.objects.all()
    modal_images = []
    for room in rooms:
        modal_images.extend(room.modal_images.split(','))
    context = {
        'rooms': rooms,
        'modal_images': modal_images,
    }
    return render(request, 'room.html', context)


def about(request):
    return render(request, 'about.html')
