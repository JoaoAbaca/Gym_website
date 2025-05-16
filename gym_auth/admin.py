from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'membership_type')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone', 'membership_type')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)