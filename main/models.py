
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth import get_user_model

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.CharField(max_length=50)
    featured = models.BooleanField(default=False)
    image = models.CharField(max_length=100, blank=True)  # Changed to CharField temporarily
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_detail', args=[str(self.id)])

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='trainers/')
    experience = models.PositiveIntegerField(null=True, blank=True)  # Now optional
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    author = models.CharField(max_length=100)
    relation = models.CharField(max_length=100)  # e.g., "Member since 2020"
    content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Testimonial by {self.author}"
    

class ClassSchedule(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_capacity = models.PositiveIntegerField(default=10)
    
    def spots_remaining(self):
        return self.max_capacity - self.booking_set.count()

class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'class_schedule')  # Prevents duplicate bookings