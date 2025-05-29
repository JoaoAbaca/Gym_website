from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm
from main.models import Booking


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required  # Now this will work
def profile(request):
    return render(request, 'registration/profile.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Add success message
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)
    
    # Get upcoming bookings
    bookings = Booking.objects.filter(
        user=user,
        class_schedule__start_datetime__gt=timezone.now()
    ).order_by('class_schedule__start_datetime')[:5]
    
    return render(request, 'profile.html', {
        'form': form,
        'bookings': bookings
    })