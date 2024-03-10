from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    beds = models.CharField(max_length=50)
    description = models.TextField()
    room_img = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    modal_name = models.CharField(max_length=50, blank=True, null=True)
    modal_description = models.TextField(blank=True, null=True)
    modal_images = models.ManyToManyField('RoomImage', related_name='rooms')
    # i want create field for adults and children
    # adults = models.IntegerField()
    # children = models.IntegerField()
    # i want create field for few rooms in one booking
    # room_capacity = models.IntegerField()






    def __str__(self):
        return self.name


class RoomImage(models.Model):
    image = models.ImageField(upload_to='static/website/img/room-slider')


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    special_request = models.TextField(blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # i want create field for few rooms in one booking
    # number_of_rooms = models.IntegerField()
    # room







# class Contact(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField()
#     message = models.TextField()

# modal_img1 = models.CharField(max_length=30, blank=True, null=True)
# modal_img2 = models.CharField(max_length=30, blank=True, null=True)
# modal_img3 = models.CharField(max_length=30, blank=True, null=True)
# modal_img4 = models.CharField(max_length=30, blank=True, null=True)
# modal_img5 = models.CharField(max_length=30, blank=True, null=True)
# modal_img6 = models.CharField(max_length=30, blank=True, null=True)
