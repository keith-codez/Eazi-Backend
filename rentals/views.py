from django.shortcuts import render
from rest_framework import viewsets 
from .models import Car, Booking
from .serializers import CarSerializer, BookingSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


