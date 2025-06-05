from django.db import models
from staff.models import Vehicle, Location
from regulator.models import Customer
from regulator.models import User
from regulator.models import Customer 
from regulator.models import Agent 


class BookingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_requests')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='booking_requests')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='booking_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    pickup_time = models.TimeField(null=True, blank=True)
    dropoff_time = models.TimeField(null=True, blank=True)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickup_requests')
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dropoff_requests', null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # NEW
    staff_notes = models.TextField(blank=True, null=True)  # NEW
    is_confirmed_by_customer = models.BooleanField(default=False) # may not be needed
    customer_docs_submitted = models.BooleanField(default=False) # may not be needed
    dummy_payment_done = models.BooleanField(default=False) # may not be needed
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(
        Agent,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='booking_requests',
        help_text="Agent who accepted this request"
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.vehicle}"
