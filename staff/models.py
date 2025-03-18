from django.contrib.auth.models import AbstractUser
from django.db import models
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


# Custom Staff model that extends AbstractUser
class Manager(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)


    def __str__(self):
        return self.username


@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    sitelink = "http://localhost:5173/"
    token = "{}".format(reset_password_token.key)
    full_link = str(sitelink)+str("password-reset/")+str(token)

    print(token)
    print(full_link)

    context = {
        'full_link':full_link,
        'email_address': reset_password_token.user.email
    }

    html_message = render_to_string("backend/email.html", context=context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        subject = "Request for resetting password for {title}".format(title=reset_password_token.user.username),
        body=plain_message,
        from_email="sender@example.com",
        to=[reset_password_token.user.email]
    )


    msg.attach_alternative(html_message, "text/html")
    msg.send()





class Vehicle(models.Model):
    OWNERSHIP_CHOICES = [
        ("company", "Company Owned"),
        ("private", "Privately Owned"),
    ]


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



class Customer(models.Model):
    TITLE_CHOICES = [
    ("MR", "Mr"),
    ("MRS", "Mrs"),
    ("MS", "Ms"),
    ("DR", "Dr"),
    ]
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default='MR')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    national_id = models.CharField(max_length=11, unique=True)
    
    # Driver’s License Image Upload
    drivers_license = models.ImageField(upload_to="drivers_licenses/", blank=True, null=True)
    
    # Next of Kin 1
    next_of_kin1_first_name = models.CharField(max_length=100)
    next_of_kin1_last_name = models.CharField(max_length=100)
    next_of_kin1_id_number = models.CharField(max_length=11)
    next_of_kin1_phone = models.CharField(max_length=15)

    # Next of Kin 2
    next_of_kin2_first_name = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin2_last_name = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin2_id_number = models.CharField(max_length=11, blank=True, null=True)
    next_of_kin2_phone = models.CharField(max_length=15, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_booking_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"