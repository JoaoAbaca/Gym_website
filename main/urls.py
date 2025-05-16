from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('trainers/', views.trainers, name='trainers'),
    path('schedule/', views.class_schedule, name='class_schedule'),
    path('book/<int:class_id>/', views.book_class, name='book_class'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]