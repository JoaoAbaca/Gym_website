from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    duration = models.CharField(max_length=50, help_text="Eg: 60 minutes")
    featured = models.BooleanField(default=False)
    image = models.CharField(max_length=100, blank=True)
    max_capacity = models.PositiveIntegerField(
        default=10,
        help_text="Maximum participants per session"
    )
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_detail', args=[str(self.id)])

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='trainers/')
    experience = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    author = models.CharField(max_length=100)
    relation = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Testimonial by {self.author}"

class ClassSchedule(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='schedules')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    max_capacity = models.PositiveIntegerField(default=10)
    
    class Meta:
        ordering = ['start_datetime']
        unique_together = [['service', 'start_datetime']]
    
    def __str__(self):
        return f"{self.service.name} with {self.trainer.name} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"
    
    def spots_remaining(self):
        return self.max_capacity - self.bookings.count()
    
    def is_available(self):
        """Check if there are spots left and if the class is in the future"""
        return self.spots_remaining() > 0 and self.start_datetime > timezone.now()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'class_schedule')
        ordering = ['class_schedule__start_datetime']
    
    def __str__(self):
        return f"{self.user.email} - {self.class_schedule}"
    
    def save(self, *args, **kwargs):
        """Ensure we don't overbook when saving"""
        if self.class_schedule.spots_remaining() <= 0:
            raise ValueError("This class is fully booked")
        super().save(*args, **kwargs)

class Membership(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    booking_limit = models.PositiveIntegerField()
    description = models.TextField()

class UserMembership(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='membership')
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()