from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Room, Booking
from datetime import datetime


# Create your views here.
def check_availability(request):
    if request.method == 'POST':
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        parsed_check_in = datetime.strptime(check_in, '%m/%d/%Y').date()
        parsed_check_out = datetime.strptime(check_out, '%m/%d/%Y').date()

        conflicting_bookings = Booking.objects.filter(check_in__lte=parsed_check_out, check_out__gte=parsed_check_in)

        if conflicting_bookings.exists():
            messages.error(request, 'Sorry, the room is not available for the selected dates. Please try again.')
            return redirect('check_availability')
        else:
            messages.success(request, 'The room is available for the selected dates. You can proceed to book it.')

            return redirect('booking' + f'?check_in={check_in}&check_out={check_out}')

    else:
        return render(request, 'check_availability.html')


def index(request):
    g = 'hello'
    return render(request, 'index.html')


def amenities(request):
    return render(request, 'amenities.html')


def contact(request):
    return render(request, 'contact.html')


# creating booking function with form
# def booking(request):
#
#     if request.method == 'GET':
#         if 'check_in' not in request.GET or 'check_out' not in request.GET:
#             return redirect('check_availability')
#         check_in = request.GET['check_in']
#         check_out = request.GET['check_out']
#
#         context = {
#             'check_in': check_in,
#             'check_out': check_out,
#
#         }
#         return render(request, 'booking.html', context)
#     elif request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         mobile = request.POST['mobile']
#         room_id = request.POST.get('room_id')
#         check_in = request.POST['check_in']
#         check_out = request.POST['check_out']
#         check_in_date = check_in.split()[0]
#         check_out_date = check_out.split()[0]
#         parsed_check_in = datetime.strptime(check_in_date, '%m/%d/%Y').date()
#         parsed_check_out = datetime.strptime(check_out_date, '%m/%d/%Y').date()
#         booking = Booking(first_name=first_name, last_name=last_name, email=email, mobile=mobile, room_id=room_id,
#                           check_in=parsed_check_in, check_out=parsed_check_out)
#         booking.save()
#         return redirect('index')
#
#     return render(request, 'booking.html')

def booking(request):
    if request.method == 'GET':
        if 'check_in' not in request.GET or 'check_out' not in request.GET  or 'room_id' not in request.GET:
            return redirect('check_availability')

        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')
        room_id = request.GET.get('room_id')

        context = {
            'check_in': check_in,
            'check_out': check_out,
            'room_id': room_id,
        }
        return render(request, 'booking.html', context)

    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        room_id = request.POST.get('room_id')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        # Convert date strings to date objects
        check_in_date = datetime.strptime(check_in.split()[0], '%m/%d/%Y').date()
        check_out_date = datetime.strptime(check_out.split()[0], '%m/%d/%Y').date()

        # Create Booking instance
        booking = Booking(first_name=first_name, last_name=last_name, email=email, mobile=mobile, room_id=room_id,
                                                    check_in=check_in_date, check_out=check_out_date)
        booking.save()
        return redirect('index')

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
        images = room.modal_images.all()
        for image in images:
            modal_images.append(image.image.url)
    context = {
        'rooms': rooms,
        'modal_images': modal_images,
    }
    return render(request, 'room.html', context)


def about(request):
    return render(request, 'about.html')

def search_available_rooms(request):
    if request.method == 'POST':
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        parsed_check_in = datetime.strptime(check_in, '%m/%d/%Y').date()
        parsed_check_out = datetime.strptime(check_out, '%m/%d/%Y').date()

        available_rooms = Room.objects.exclude(booking__check_in__lte=parsed_check_out, booking__check_out__gte=parsed_check_in)

        return render(request, 'search_available_rooms.html', {'available_rooms': available_rooms, 'check_in': check_in, 'check_out': check_out})
    else:
        return render(request, 'search_available_rooms.html')