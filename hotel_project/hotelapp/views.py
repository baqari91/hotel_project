from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Room, Booking
from datetime import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.


def search_available_rooms(request):
    if request.method == 'POST':
        # Get check-in and check-out dates
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        parsed_check_in = datetime.strptime(check_in, '%m/%d/%Y').date()  # Convert string to date object
        parsed_check_out = datetime.strptime(check_out, '%m/%d/%Y').date()  # Convert string to date object

        # Get available rooms
        available_rooms = Room.objects.exclude(booking__check_in__lte=parsed_check_out,
                                               booking__check_out__gte=parsed_check_in)

        # Get modal images for each room
        modal_images = []
        for room in available_rooms:
            images = room.modal_images.all()
            for image in images:
                modal_images.append(image.image.url)

        # If available rooms exist, display them
        if available_rooms.exists():
            messages.success(request, 'The following rooms are available for the selected dates.')
            context = {
                'available_rooms': available_rooms,
                'check_in': check_in,
                'check_out': check_out,
            }
            return render(request, 'search_available_rooms.html', context)
        else:
            messages.error(request, 'Sorry, no rooms are available for the selected dates. Please try again.')
            return redirect('search_available_rooms')
    else:
        return render(request, 'search_available_rooms.html')


def booking(request):
    if request.method == 'GET':
        # Check if the required parameters are in the URL
        if 'check_in' not in request.GET or 'check_out' not in request.GET or 'room_id' not in request.GET:
            return redirect('search_available_rooms')

        # Get the check-in, check-out dates and room_id from the URL
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')
        room_id = request.GET.get('room_id')

        context = {
            'check_in': check_in,
            'check_out': check_out,
            'room_id': room_id,
        }
        # Render the booking page with the check-in, check-out dates and room_id
        return render(request, 'booking.html', context)

    elif request.method == 'POST':
        user = request.user
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
        booking = Booking(user=user, first_name=first_name, last_name=last_name, email=email, mobile=mobile,
                          room_id=room_id,
                          check_in=check_in_date, check_out=check_out_date)
        booking.save()
        return redirect('profile')
    else:
        return render(request, 'booking.html')


def change_booking(request):
    if request.method == 'GET':
        # Check if the required parameters are in the URL
        if ('check_in' not in request.GET or 'check_out' not in request.GET or 'booking_id' not in request.GET or
                'room_id' not in request.GET):
            return redirect('profile')

        # Get the check-in, check-out dates and room_id from the URL
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')
        room_id = request.GET.get('room_id')
        booking_id = request.GET.get('booking_id')

        # check availability
        parsed_check_in = datetime.strptime(check_in, '%m/%d/%Y').date()
        parsed_check_out = datetime.strptime(check_out, '%m/%d/%Y').date()

        # check if the room is available for the selected dates without the current booking
        conflicting_bookings = Booking.objects.filter(check_in__lte=parsed_check_out,
                                                      check_out__gte=parsed_check_in).exclude(id=booking_id)
        if conflicting_bookings.exists():
            messages.error(request, 'Sorry, the room is not available for the selected dates. Please try again.')
            return redirect('profile')

        else:
            messages.success(request, 'The room is available for the selected dates. You can proceed to change it.')

            context = {
                'check_in': check_in,
                'check_out': check_out,
                'room_id': room_id,
                'booking_id': booking_id,
            }
            # Render the booking page with the check-in, check-out dates and room_id
            return render(request, 'change_booking.html', context)

    elif request.method == 'POST':
        user = request.user
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

        # Create Booking instance with the new details
        booking = Booking(user=user, first_name=first_name, last_name=last_name, email=email, mobile=mobile,
                          room_id=room_id,
                          check_in=check_in_date, check_out=check_out_date)
        booking.save()

        # Delete the old booking
        booking_id = request.POST.get('booking_id')
        old_booking = Booking.objects.get(id=booking_id)
        old_booking.delete()

        # Redirect to the profile page with message
        messages.error(request, 'Booking changed successfully')
        return redirect('profile')
    else:
        return render(request, 'change_booking.html')


def booking_delete(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.delete()
    return redirect('profile')


@login_required
def profile(request):
    # filter bookings by the current user and order them by past and future bookings
    future_bookings = Booking.objects.filter(user=request.user, check_in__gte=datetime.now().date()).order_by(
        'check_in')
    past_bookings = Booking.objects.filter(user=request.user, check_in__lt=datetime.now().date()).order_by('-check_in')
    user_booking = list(future_bookings) + list(past_bookings)

    # decide how many times until the check-in date
    for booking in user_booking:
        days_until_check_in = (booking.check_in - datetime.now().date()).days
        booking.days_until_check_in = days_until_check_in

    # format the days_until_check_in to be more user-friendly
    for booking in user_booking:
        if booking.days_until_check_in == 0:
            booking.days_until_check_in = 'Today'
        elif booking.days_until_check_in == 1:
            booking.days_until_check_in = 'Tomorrow'
        elif 1 < booking.days_until_check_in < 14:
            booking.days_until_check_in = f'In {booking.days_until_check_in} days'
        elif booking.days_until_check_in == -1:
            booking.days_until_check_in = 'Yesterday'
        elif 14 < booking.days_until_check_in < 21:
            booking.days_until_check_in = 'In 2 weeks'
        elif 21 < booking.days_until_check_in < 28:
            booking.days_until_check_in = 'In 3 weeks'
        elif 28 < booking.days_until_check_in < 35:
            booking.days_until_check_in = 'In 1 month'
        elif 35 < booking.days_until_check_in < 42:
            days = booking.days_until_check_in - 30
            booking.days_until_check_in = f'In 1 month and {days} days'
        elif 42 < booking.days_until_check_in < 49:
            days = booking.days_until_check_in - 30
            if days > 7:
                booking.days_until_check_in = f'In 1 month and 1 week'
        elif 49 < booking.days_until_check_in < 56:
            days = booking.days_until_check_in - 30
            if days > 14:
                booking.days_until_check_in = f'In 1 month and 2 weeks'
        elif 56 < booking.days_until_check_in < 63:
            days = booking.days_until_check_in - 30
            if days > 21:
                booking.days_until_check_in = f'In 1 month and 3 weeks'
        elif 63 < booking.days_until_check_in < 70:
            booking.days_until_check_in = f'In 2 months'
        elif 70 < booking.days_until_check_in < 100:
            booking.days_until_check_in = f'In 3 months'
        elif 100 < booking.days_until_check_in < 130:
            booking.days_until_check_in = f'In 4 months'
        elif 130 < booking.days_until_check_in < 160:
            booking.days_until_check_in = f'In 5 months'
        elif 160 < booking.days_until_check_in < 190:
            booking.days_until_check_in = f'In 6 months'
        elif 190 < booking.days_until_check_in < 250:
            booking.days_until_check_in = f'In 8 months'
        elif 250 < booking.days_until_check_in < 300:
            booking.days_until_check_in = f'In 10 months'
        elif 300 < booking.days_until_check_in < 360:
            booking.days_until_check_in = f'In 1 year'
        elif 360 < booking.days_until_check_in < 720:
            booking.days_until_check_in = f'In 2 years'
        elif 720 < booking.days_until_check_in < 1080:
            booking.days_until_check_in = f'In 3 years'
        elif 1080 < booking.days_until_check_in < 1440:
            booking.days_until_check_in = f'In 4 years'

        else:
            if booking.days_until_check_in > -14:
                booking.days_until_check_in = f'{abs(booking.days_until_check_in)} days ago'
            elif booking.days_until_check_in > -21:
                booking.days_until_check_in = f'3 week ago'
            elif booking.days_until_check_in > -28:
                booking.days_until_check_in = f'1 month ago'
            elif booking.days_until_check_in > -58:
                booking.days_until_check_in = f'2 months ago'
            elif booking.days_until_check_in > -88:
                booking.days_until_check_in = f'3 months ago'
            elif booking.days_until_check_in > -118:
                booking.days_until_check_in = f'4 months ago'
            elif booking.days_until_check_in > -148:
                booking.days_until_check_in = f'5 months ago'
            elif booking.days_until_check_in > -178:
                booking.days_until_check_in = f'6 months ago'
            elif booking.days_until_check_in > -208:
                booking.days_until_check_in = f'7 months ago'
            elif booking.days_until_check_in > -238:
                booking.days_until_check_in = f'8 months ago'
            elif booking.days_until_check_in > -268:
                booking.days_until_check_in = f'9 months ago'
            elif booking.days_until_check_in > -298:
                booking.days_until_check_in = f'10 months ago'
            elif booking.days_until_check_in > -328:
                booking.days_until_check_in = f'11 months ago'
            elif booking.days_until_check_in > -358:
                booking.days_until_check_in = f'1 year ago'
            elif booking.days_until_check_in > -718:
                booking.days_until_check_in = f'2 years ago'
            elif booking.days_until_check_in > -1078:
                booking.days_until_check_in = f'3 years ago'
            elif booking.days_until_check_in > -1438:
                booking.days_until_check_in = f'4 years ago'
            else:
                booking.days_until_check_in = f'{abs(booking.days_until_check_in)} days ago'

    # totall price of booking
    for booking in user_booking:
        price = booking.room.price
        check_in = booking.check_in
        check_out = booking.check_out
        days = (check_out - check_in).days
        total_price = price * days
        booking.total_price = f'${total_price}'

    # booking status uppcoming or past
    if user_booking:
        for booking in user_booking:
            if booking.check_in > datetime.now().date():
                booking.status = 'Upcoming'
            else:
                booking.status = 'Past'

    # Reserved days
    for booking in user_booking:
        check_in = booking.check_in
        check_out = booking.check_out
        days = (check_out - check_in).days
        booking.reserved_days = f'{days} days'

    context = {
        'future_bookings': future_bookings,
        'past_bookings': past_bookings,
        'user_bookings': user_booking,
    }
    return render(request, 'profile.html', context)


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


def index(request):
    g = 'hello'
    return render(request, 'index.html')


def amenities(request):
    return render(request, 'amenities.html')


def contact(request):
    return render(request, 'contact.html')
