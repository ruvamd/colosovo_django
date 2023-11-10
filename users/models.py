# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # Add custom fields if needed
    # Example:
    # bio = models.TextField(max_length=500, blank=True)
    pass
