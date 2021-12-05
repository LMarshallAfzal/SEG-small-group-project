from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
from django.contrib.auth.models import Group

class User(AbstractUser):
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'
    first_name = models.CharField(max_length = 50, blank = False)
    last_name = models.CharField(max_length = 50, blank = False)
    email = models.EmailField(unique = True, blank = False)
    bio = models.CharField(max_length = 520, blank = True)
    EXPERIENCE_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]
    experience_level = models.CharField(max_length = 12, choices = EXPERIENCE_CHOICES, default = BEGINNER)
    personal_statement = models.CharField(max_length = 1250, blank = True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=800):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)

    def approve_applicant(self, user, club_codename):
        """Change the group from applicant to member"""
        member = Group.objects.get(name = club_codename + " Member")
        member.user_set.add(user)
        applicant_group = Group.objects.get(name = club_codename + " Applicant")
        applicant_group.user_set.remove(user)



class Club(models.Model):
    club_name = models.CharField(max_length = 50, blank = False, unique = True)
    club_codename = models.CharField(max_length = 50, blank = False, unique = True)

    def create_groups_and_permissions_for_club(self):
        from .groups import ChessClubGroups
        club_groups_and_permissions = ChessClubGroups(self.club_codename)

    def getGroupsForClub(self):
        return [self.getClubApplicantGroup(), self.getClubMemberGroup(), self.getClubOfficerGroup(), self.getClubOwnerGroup()]

    def getClubApplicantGroup(self):
        return Group.objects.get(name = self.club_codename + " Applicant")

    def getClubMemberGroup(self):
        return Group.objects.get(name = self.club_codename + " Member")

    def getClubOfficerGroup(self):
        return Group.objects.get(name = self.club_codename + " Officer")

    def getClubOwnerGroup(self):
        return Group.objects.get(name = self.club_codename + " Owner")
