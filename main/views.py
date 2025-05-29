from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service, Trainer, Testimonial, ClassSchedule, Booking
from .forms import ContactForm  # We'll create this form next
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ContactForm, ClassScheduleForm 


def home(request):
    featured_services = Service.objects.filter(featured=True)
    testimonials = Testimonial.objects.filter(approved=True)
    return render(request, 'home.html', {
        'featured_services': featured_services,
        'testimonials': testimonials
    })

def about(request):
    trainers = Trainer.objects.all()
    return render(request, 'about.html', {'trainers': trainers})

def services(request):
    all_services = Service.objects.all()
    return render(request, 'services.html', {'services': all_services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    # Get available schedules
    schedules = ClassSchedule.objects.filter(
        service=service,
        start_datetime__gt=timezone.now()
    ).order_by('start_datetime')
    
    return render(request, 'service_detail.html', {
        'service': service,
        'schedules': schedules
    })

def trainers(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainers.html', {'trainers': trainers})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Send email (configure email settings in production)
            send_mail(
                f'Contact Form Submission from {name}',
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return redirect('contact_success')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')

def schedule(request):
    # Get upcoming classes (next 7 days)
    start_date = timezone.now()
    end_date = start_date + timedelta(days=7)
    
    schedules = ClassSchedule.objects.filter(
        start_datetime__range=(start_date, end_date),
        start_datetime__gt=timezone.now()
    ).order_by('start_datetime')
    
    return render(request, 'schedule.html', {'schedules': schedules})

@login_required
def book_class(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    
    # Check if class is available
    if not schedule.is_available():
        return render(request, 'booking_error.html', {
            'error': 'This class is fully booked'
        })
    
    # Check if user already booked this class
    if Booking.objects.filter(user=request.user, class_schedule=schedule).exists():
        return render(request, 'booking_error.html', {
            'error': 'You already booked this class'
        })
    
    # Create booking
    Booking.objects.create(user=request.user, class_schedule=schedule)
    
    return redirect('my_bookings')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user,
        class_schedule__start_datetime__gt=timezone.now()
    ).order_by('class_schedule__start_datetime')
    
    return render(request, 'bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('my_bookings')

@login_required
def book_class(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    
    # Check if class is available
    if not schedule.is_available():
        messages.error(request, "This class is fully booked")
        return redirect('service_detail', service_id=schedule.service.id)
    
    # Check if user already booked this class
    if Booking.objects.filter(user=request.user, class_schedule=schedule).exists():
        messages.warning(request, "You've already booked this class")
        return redirect('service_detail', service_id=schedule.service.id)
    
    # Create booking
    Booking.objects.create(user=request.user, class_schedule=schedule)
    messages.success(request, "Class booked successfully!")
    return redirect('my_bookings')

@login_required
def my_bookings(request):
    # Get upcoming bookings only
    bookings = Booking.objects.filter(
        user=request.user,
        class_schedule__start_datetime__gt=timezone.now()
    ).order_by('class_schedule__start_datetime')
    
    return render(request, 'bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Booking canceled successfully")
    return redirect('my_bookings')

@staff_member_required
def admin_dashboard(request):
    # Show upcoming classes and booking stats
    upcoming_classes = ClassSchedule.objects.filter(
        start_datetime__gt=timezone.now()
    ).order_by('start_datetime')[:10]
    
    recent_bookings = Booking.objects.select_related(
        'class_schedule', 'user'
    ).order_by('-booked_at')[:10]
    
    return render(request, 'admin/dashboard.html', {
        'upcoming_classes': upcoming_classes,
        'recent_bookings': recent_bookings
    })

@staff_member_required
def manage_schedules(request):
    schedules = ClassSchedule.objects.filter(
        start_datetime__gt=timezone.now()
    ).order_by('start_datetime')
    
    return render(request, 'admin/manage_schedules.html', {
        'schedules': schedules
    })

@staff_member_required
def add_schedule(request):
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class schedule added successfully!")
            return redirect('manage_schedules')
    else:
        form = ClassScheduleForm()
    
    return render(request, 'admin/schedule_form.html', {
        'form': form,
        'title': 'Add New Class Schedule'
    })

@staff_member_required
def edit_schedule(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule updated successfully!")
            return redirect('manage_schedules')
    else:
        form = ClassScheduleForm(instance=schedule)
    
    return render(request, 'admin/schedule_form.html', {
        'form': form,
        'title': 'Edit Class Schedule'
    })

@staff_member_required
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, "Schedule deleted successfully!")
        return redirect('manage_schedules')
    
    return render(request, 'admin/confirm_delete.html', {
        'object': schedule,
        'type': 'class schedule'
    })

@staff_member_required
def view_bookings(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    bookings = Booking.objects.filter(class_schedule=schedule)
    
    return render(request, 'admin/view_bookings.html', {
        'schedule': schedule,
        'bookings': bookings
    })

@staff_member_required
def add_schedule(request):
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST)  # Now defined
        if form.is_valid():
            form.save()
            messages.success(request, "Class schedule added successfully!")
            return redirect('manage_schedules')
    else:
        form = ClassScheduleForm()
    
    return render(request, 'admin/schedule_form.html', {
        'form': form,
        'title': 'Add New Class Schedule'
    })

@staff_member_required
def edit_schedule(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST, instance=schedule)  # Now defined
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule updated successfully!")
            return redirect('manage_schedules')
    else:
        form = ClassScheduleForm(instance=schedule)
    
    return render(request, 'admin/schedule_form.html', {
        'form': form,
        'title': 'Edit Class Schedule'
    })