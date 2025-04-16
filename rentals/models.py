from django.db import models
from staff.models import Vehicle, Customer 



class Lead(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class BookingRequest(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='booking_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.last_name} - {self.vehicle}"


