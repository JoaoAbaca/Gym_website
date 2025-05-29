# main/forms.py

from django import forms
from .models import ClassSchedule
from django.utils import timezone


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your Name',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email',
        'class': 'form-control'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Your Message',
        'class': 'form-control',
        'rows': 5
    }))



class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['service', 'trainer', 'start_datetime', 'end_datetime', 'max_capacity']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')
        
        if start_datetime and end_datetime:
            # Ensure start time is in the future
            if start_datetime < timezone.now():
                self.add_error('start_datetime', "Start time cannot be in the past")
            
            # Ensure end time is after start time
            if end_datetime <= start_datetime:
                self.add_error('end_datetime', "End time must be after start time")
        
        return cleaned_data