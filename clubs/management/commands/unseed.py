from django.core.management.base import BaseCommand, CommandError
from clubs.models import User
from clubs.club_list import ClubList, Club
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.filter(is_staff=False, is_superuser=False).delete()

        for perm in Permission.objects.all():
            perm.delete()
        for group in Group.objects.all():
            group.delete()
        ClubList.club_list.clear() #Deletes all clubs
