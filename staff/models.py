from django.contrib.auth.models import AbstractUser
from django.db import models
# Custom Staff model that extends AbstractUser
class Manager(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)


    def __str__(self):
        return self.username
