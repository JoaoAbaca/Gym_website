from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Booking

@receiver(post_save, sender=Booking)
def send_booking_confirmation(sender, instance, created, **kwargs):
    if created:
        subject = f"Class Booking Confirmation: {instance.class_schedule.service.name}"
        message = (
            f"Hello {instance.user.first_name},\n\n"
            f"You've successfully booked:\n"
            f"Service: {instance.class_schedule.service.name}\n"
            f"Date: {instance.class_schedule.start_datetime.strftime('%A, %B %d')}\n"
            f"Time: {instance.class_schedule.start_datetime.strftime('%H:%M')} - "
            f"{instance.class_schedule.end_datetime.strftime('%H:%M')}\n"
            f"Trainer: {instance.class_schedule.trainer.name}\n\n"
            "You can view and manage your bookings in your profile.\n\n"
            "Best regards,\nPowerFit Gym Team"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=False,
        )