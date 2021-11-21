"""Configuration of the admin interface for clubs"""
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Confuguration of the admin interface for users."""
    list_display = [
    'id', 'first_name', 'last_name', 'email', 'bio', 'experience_level', 'personal_statement',
    ]
