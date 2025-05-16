
from django.shortcuts import render
from .models import Service, Trainer  
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import ClassSchedule, Booking


def home(request):
    featured_services = Service.objects.filter(featured=True)[:3]
    trainers = Trainer.objects.all()[:4]
    context = {
        'featured_services': featured_services,
        'trainers': trainers
    }
    return render(request, 'home.html', context)

def services(request):
    all_services = Service.objects.all()  # Get all services from database
    return render(request, 'services.html', {'services': all_services})

def service_detail(request, pk):
    service = Service.objects.get(id=pk)
    return render(request, 'service_detail.html', {'service': service})

def about(request):
    trainers = Trainer.objects.all()  # Reuse your Trainer model
    return render(request, 'about.html', {'trainers': trainers})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Build the email message
            email_message = f"""
            From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>
            Phone: {form.cleaned_data['phone'] or 'Not provided'}
            
            Message:
            {form.cleaned_data['message']}
            """
            
            send_mail(
                subject=f"New contact from {form.cleaned_data['name']}",
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return render(request, 'contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')

def trainers(request):
    all_trainers = Trainer.objects.all()
    return render(request, 'trainers.html', {'trainers': all_trainers})

@login_required
def book_class(request, class_id):
    class_schedule = ClassSchedule.objects.get(id=class_id)
    if class_schedule.spots_remaining() > 0:
        Booking.objects.get_or_create(
            user=request.user,
            class_schedule=class_schedule
        )
        return redirect('my_bookings')
    return redirect('class_schedule')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings.html', {'bookings': bookings})

@login_required  # Add this decorator
def class_schedule(request):
    classes = ClassSchedule.objects.all()
    return render(request, 'schedule.html', {'classes': classes})