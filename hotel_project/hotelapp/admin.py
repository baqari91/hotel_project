from django.contrib import admin
from .models import Booking, Room, RoomImage

# Register your models here.
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(RoomImage)

