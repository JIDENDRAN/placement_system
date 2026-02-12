from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, AlumniProfile

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('role', 'phone_number', 'profile_picture', 'bio')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(AlumniProfile)
