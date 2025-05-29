from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('manage-schedules/', views.manage_schedules, name='manage_schedules'),
    path('add-schedule/', views.add_schedule, name='add_schedule'),
    path('edit-schedule/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('delete-schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('view-bookings/<int:schedule_id>/', views.view_bookings, name='view_bookings'),
]