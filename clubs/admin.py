"""Configuration of the admin interface for clubs"""
from django.contrib import admin
from .models import User, Club
from .club_list import ClubList

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Confuguration of the admin interface for users."""
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)
    group.short_description = 'Groups'

    list_display = [
    'id', 'first_name', 'last_name', 'email', 'bio', 'experience_level', 'personal_statement' ,'group'
    ]
