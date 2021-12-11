from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
from django.contrib.auth.models import Group
import clubs.helpers as h

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

    class Meta:
        """Model options."""

        ordering = ('last_name','first_name')

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

    # def approve_applicant(self, user, club_codename):
    #     """Change the group from applicant to member"""
    #     member = Group.objects.get(name = club_codename + " Member")
    #     member.user_set.add(user)
    #     applicant_group = Group.objects.get(name = club_codename + " Applicant")
    #     applicant_group.user_set.remove(user)


class ClubManager(models.Manager):
    def create_club(self, name, mission_statement, location):
        club = self.create(club_name = name, club_codename = h.convert_to_codename(name), mission_statement = mission_statement, club_location = location)
        club.create_groups_and_permissions_for_club()
        return club

class Club(models.Model):
    club_name = models.CharField(max_length = 50, blank = False, unique = True)
    club_codename = models.CharField(max_length = 50, blank = False, unique = True)
    mission_statement = models.CharField(max_length = 150, blank = True, unique = False)
    club_location = models.CharField(max_length = 50, blank = True, unique = False)
    member_count = models.PositiveIntegerField(default = 0)
    objects = ClubManager()

    def get_club_details(self):
        owner = User.objects.filter(groups__name = self.club_codename + " Owner")[0] #There should only be one owner
        return [self.club_name, self.club_location, self.mission_statement, (owner.first_name + owner.last_name), owner.bio, owner.gravatar()]

    def create_groups_and_permissions_for_club(self):
        from .groups import ChessClubGroups
        club_groups_and_permissions = ChessClubGroups(self.club_codename)

    def get_user_role_in_club(self, user):
        if user.groups.filter(name = self.club_codename + " Applicant").exists():
            return "Applicant"
        elif user.groups.filter(name = self.club_codename + " Member").exists():
            return "Member"
        elif user.groups.filter(name = self.club_codename + " Officer").exists():
            return "Officer"
        elif user.groups.filter(name = self.club_codename + " Owner").exists():
            return "Owner"
        else:
            return None #If the user is not part of the club this will be returned

    #Includes failsafe to switch the role of the user in the club if they werw already in the club
    def add_user_to_club(self, user, initial_role):
        if self.get_user_role_in_club(user) == None:
            user.groups.add(Group.objects.get(name = self.club_codename + " " + initial_role))
            if initial_role == "Member":
                self.member_count += 1
        else:
            self.switch_user_role_in_club(user, initial_role)

    #Will not add users to a club if they were not in the club to begin with.
    def switch_user_role_in_club(self, user, new_role):
        old_role = self.get_user_role_in_club(user)
        if old_role != None:
            user.groups.remove(user.groups.filter(name = self.club_codename + " " + old_role)[0])
            user.groups.add(Group.objects.get(name = self.club_codename + " " + new_role))
            if old_role == "Member":
                self.member_count -= 1
            if new_role == "Member":
                self.member_count += 1
            return True
        return False

    def remove_user_from_club(self, user):
        old_role = self.get_user_role_in_club(user)
        if old_role != None:
            user.groups.remove(user.groups.filter(name = self.club_codename + " " + old_role)[0])
            if old_role == "Member":
                self.member_count -= 1

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
