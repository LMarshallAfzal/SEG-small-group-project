from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Club
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.filter(is_staff=False, is_superuser=False).delete()
        for perm in Permission.objects.all():
            perm.delete()
        for group in Group.objects.all():
            group.delete()
        for club in Club.objects.all():
            club.delete()
