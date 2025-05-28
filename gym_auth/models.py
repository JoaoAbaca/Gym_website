from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    membership_type = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.email
        # Add these to resolve conflicts:
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name="customuser_groups",  # UNIQUE related name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name="customuser_permissions",  # UNIQUE related name
        related_query_name="user",
    )