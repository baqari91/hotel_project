from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('check_availability', views.check_availability, name='check_availability'),
    path('contact', views.contact, name='contact'),
    path('booking', views.booking, name='booking'),
    path('login', views.login, name='login'),
    path('room', views.room, name='room'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('search_available_rooms', views.search_available_rooms, name='search_available_rooms'),

]
