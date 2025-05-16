from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    membership_type = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.email