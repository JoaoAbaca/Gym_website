from django.contrib import admin

from .models import ClassSchedule, Booking

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('service', 'date', 'start_time', 'trainer', 'spots_remaining')

admin.site.register(Booking)
