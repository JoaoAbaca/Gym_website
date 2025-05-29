from django.contrib import admin
from .models import Service, Trainer, Testimonial, ClassSchedule, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'max_capacity', 'featured')
    search_fields = ('name',)

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience')
    search_fields = ('name', 'specialization')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'relation', 'rating', 'approved')
    list_editable = ('approved',)
    list_filter = ('approved', 'rating')
    search_fields = ('author', 'content')

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'service', 
        'trainer', 
        'start_datetime',  # Changed from 'date'
        'end_datetime',    # Changed from 'start_time'
        'max_capacity', 
        'spots_remaining', 
        'is_available'
    )
    list_filter = ('service', 'trainer', 'start_datetime')
    search_fields = ('service__name', 'trainer__name')
    date_hierarchy = 'start_datetime'  # Changed from 'date'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_schedule', 'booked_at')
    list_filter = ('class_schedule__service', 'booked_at')
    search_fields = ('user__email', 'class_schedule__service__name')