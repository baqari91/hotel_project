from django.db import models


# Create your models here.

# i want to create a model for the rooms
# i want to create a model for the booking
# i want to create a model for the availability of the rooms
# i want to create a model for the userprofile
# i want to create a model for the contact form
# i want to create a model for the amenities
# i want to create a model for the gallery

class Room(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    beds = models.CharField(max_length=50)
    description = models.TextField()
    room_img = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    modal_name = models.CharField(max_length=50, blank=True, null=True)
    modal_description = models.TextField(blank=True, null=True)
    modal_images = models.TextField(blank=True, null=True)

    # modal_img1 = models.CharField(max_length=30, blank=True, null=True)
    # modal_img2 = models.CharField(max_length=30, blank=True, null=True)
    # modal_img3 = models.CharField(max_length=30, blank=True, null=True)
    # modal_img4 = models.CharField(max_length=30, blank=True, null=True)
    # modal_img5 = models.CharField(max_length=30, blank=True, null=True)
    # modal_img6 = models.CharField(max_length=30, blank=True, null=True)


class Booking(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    special_request = models.TextField(blank=True, null=True)


class Availability(models.Model):
    foreign_key = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_guests = models.IntegerField()
    room = models.IntegerField()
    availability = models.BooleanField()


# class Contact(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField()
#     message = models.TextField()

