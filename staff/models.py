from django.contrib.auth.models import AbstractUser,  Group, Permission
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import os
from django.conf import settings
from rest_framework.authtoken.models import Token
from regulator.models import Customer, Agent, Agency




class Location(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=100, blank=True)  # For maps (optional)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    OWNERSHIP_CHOICES = [
        ("company", "Company Owned"),
        ("private", "Privately Owned"),
    ]

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="vehicles")
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacture_year = models.PositiveIntegerField()  # New field
    color = models.CharField(max_length=50)
    mileage = models.PositiveIntegerField()
    mileage_allowance = models.PositiveIntegerField(default=0)  # New field
    ownership = models.CharField(max_length=10, choices=OWNERSHIP_CHOICES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field
    maintenance_records = models.TextField(blank=True, null=True)
    registration_number = models.CharField(max_length=20, unique=True)
    next_service_date = models.DateField(blank=True, null=True)  # New field
    pickup_locations = models.ManyToManyField('Location', related_name='vehicles')

    def __str__(self):
        return f"{self.make} {self.model} {self.color} ({self.registration_number})"

        
class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="vehicle_images/")

    def __str__(self):
        return f"Image for {self.vehicle.make} {self.vehicle.model}"




class MaintenanceRecord(models.Model):
    
    vehicle = models.ForeignKey(Vehicle, related_name="maintenance_entries", on_delete=models.CASCADE)  # Fix conflict
    date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Maintenance for {self.vehicle.brand} {self.vehicle.model} on {self.date}"



class VehicleUnavailability(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="unavailable_periods")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, choices=[("maintenance", "Maintenance"),("booking", "Booking"), ("other", "Other")], default="other")


    def __str__(self):
        return f"{self.vehicle.make} {self.vehicle.model} unavailable from {self.start_date} to {self.end_date}"





class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="bookings")
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[("mobile transfer", "Mobile Transfer"), ("debit card", "Debit Card"), ("cash", "Cash")], default="cash") 
    booking_status = models.CharField(max_length=20, choices=[("confirmed", "Confirmed"), ("pending", "Pending"), ("completed", "Completed"), ("active", "Active"), ("canceled", "Canceled")], default="pending")
    estimated_mileage = models.PositiveIntegerField(default=0)
    destination = models.CharField(max_length=255, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_description = models.TextField(blank=True, null=True)
    pickup_location = models.CharField(max_length=255, blank=True, null=True)
    dropoff_location = models.CharField(max_length=255, blank=True, null=True)
    pickup_time = models.TimeField(blank=True, null=True)
    dropoff_time = models.TimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.customer} - {self.vehicle} from {self.start_date} to {self.end_date}"
    
    


