from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Booking
from django.utils import timezone
from datetime import datetime,timedelta

@receiver(post_save, sender=Booking)
def send_booking_confirmation(sender, instance, created, **kwargs):
    if created:
        # Send confirmation email
        send_mail(
            f'Booking Confirmation: {instance.class_schedule.service.name}',
            f'Hello {instance.user.first_name},\n\n'
            f'Your booking for {instance.class_schedule.service.name} on '
            f'{instance.class_schedule.start_datetime.strftime("%B %d, %Y at %H:%M")} is confirmed.\n\n'
            'Thank you for choosing PowerFit Gym!',
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=False,
        )
        
        # Schedule reminder email (24h before class)
        reminder_time = instance.class_schedule.start_datetime - timedelta(hours=24)
        if reminder_time > timezone.now():
            schedule_email(
                'Class Reminder',
                f'Reminder: Your {instance.class_schedule.service.name} class is tomorrow at '
                f'{instance.class_schedule.start_datetime.strftime("%H:%M")}',
                settings.DEFAULT_FROM_EMAIL,
                [instance.user.email],
                reminder_time
            )