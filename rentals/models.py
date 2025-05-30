from django.db import models
from staff.models import Vehicle
from regulator.models import Customer
from regulator.models import User


class BookingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_requests')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='booking_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # NEW
    staff_notes = models.TextField(blank=True, null=True)  # NEW

    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.vehicle}"
