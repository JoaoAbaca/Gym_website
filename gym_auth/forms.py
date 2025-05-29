from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm  # ADD PasswordChangeForm
from .models import CustomUser
import re

def validate_id_number(value):
    """Validate that the ID number is numeric and 8-12 digits long"""
    if not re.match(r'^\d{8,12}$', value):
        raise forms.ValidationError(
            'ID number must be 8-12 digits long and contain only numbers.'
        )

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Your ID number will be your initial password. You can change it later.",
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'ID Number',
        }
        help_texts = {
            'username': 'Your national ID or passport number (8-12 digits)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial password to username (ID number)
        if self.instance and self.instance.username:
            self.fields['password1'].initial = self.instance.username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Set password to ID number
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].help_text = "Your current password (initially your ID number)"