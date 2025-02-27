from django.db import models
from django.utils import timezone
# Create your models here.


class Car(models.Model):
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=10)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.registration_number})"
    
class Booking(models.Model):
     car = models.ForeignKey(Car, on_delete=models.CASCADE)
     customer_name = models.CharField(max_length=200)
     customer_email = models.EmailField()
     customer_phone = models.CharField(max_length=15)
     start_date = models.DateField()
     end_date = models.DateField()
     total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
     status = models.CharField(
         max_length=20,
         choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
         default='Pending'
     )
     def _str__(self):
         return f"{self.car} - {self.customer_name} ({self.start_date} to {self.end_date})"
     
class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)  # Add 'related_name' to avoid reverse accessor clashes
    image = models.ImageField(upload_to='cars/')
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Image for {self.car.make} {self.car.model}"