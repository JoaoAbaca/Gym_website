from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_id_number(value):
    """Validate that the ID number is numeric and 8-12 digits long"""
    if not re.match(r'^\d{8,12}$', value):
        raise ValidationError(
            'ID number must be 8-12 digits long and contain only numbers.'
        )

class CustomUser(AbstractUser):

    username = models.CharField(
        max_length=12,
        unique=True,
        validators=[validate_id_number],
        verbose_name='ID Number',
        help_text='Required. 8-12 digits only.'
    )
    

    email = models.EmailField(blank=True, null=True)
    

    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    def clean(self):
        super().clean()
        validate_id_number(self.username)