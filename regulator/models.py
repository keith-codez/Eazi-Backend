from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("agent", "Agent"),
        ("agency", "Agency"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', null=True, blank=True)
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
    national_id = models.CharField(max_length=30, null=True, blank=True, unique=False)  # remove unique=True
    street_address = models.CharField(max_length=255, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)

    related_agent = models.ForeignKey(
        'regulator.Agent',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='customers'
    )
    related_agency = models.ForeignKey(
        'regulator.Agency',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='customers'
    )
    is_public_only = models.BooleanField(default=True)
    
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

    def delete_drivers_license(self):
        """Deletes the driver's license file from storage"""
        if self.drivers_license:
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.drivers_license))
            if os.path.exists(image_path):
                os.remove(image_path)
            self.drivers_license = None
            self.save()



class Agency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    number_of_employees = models.IntegerField(default=1)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agency_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    first_name = models.CharField(max_length=100, null=True,)
    last_name = models.CharField(max_length=100, null=True,)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True, related_name='agents')
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username