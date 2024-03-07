from django.contrib import admin
from .models import Room, RoomImage, Booking

# Register your models here.
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(RoomImage)

