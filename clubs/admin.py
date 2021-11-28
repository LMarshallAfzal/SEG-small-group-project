"""Configuration of the admin interface for clubs"""
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User

admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Confuguration of the admin interface for users."""
    list_display = [
    'id', 'first_name', 'last_name', 'email', 'bio', 'experience_level', 'personal_statement',
    ]
    list_filter = ['group','experience_level']
    search_fields = ['id','first_name','last_name']


class ClubAdmin(admin.AdminSite):
    list_display = [
    'id', 'first_name', 'last_name', 'email', 'bio', 'experience_level', 'personal_statement',
    ]
    list_editable = ['group']
    index_title = "The Chess Club"
    site_header = "Club Owner"
    site_title = "Manage the Chess Club"

club_owner_site = ClubAdmin(name = 'ClubAdmins')
club_owner_site.register(User)
club_owner_site.register(Group)