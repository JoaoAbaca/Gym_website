from django.urls import path
from . import views
from gym_auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('trainers/', views.trainers, name='trainers'),  # Added missing trainers URL
    path('schedule/', views.schedule, name='schedule'),  # Added missing schedule URL
    path('contact/', views.contact, name='contact'),
    path('book/<int:schedule_id>/', views.book_class, name='book_class'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('schedule/calendar/', views.ScheduleCalendarView.as_view(), name='schedule_calendar'),
    path('profile/', auth_views.profile, name='profile'),
    # Removed admin/bulk-add-schedule (it belongs in urls_admin)
]