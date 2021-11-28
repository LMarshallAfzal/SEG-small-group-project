from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

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


    #Defines custom permissions for users to be added to the database.
    #This assumes that Users include applicants, members, officers and the owner,
    #permissions will be granted based on which type of user they are
    #Admin = superuser = all permissions granted
    class Meta:
        permissions = [
            ('can_access_member_list', 'Can access a basic list of members and some details'),
            ('can_access_full_member_list', 'Can access list of members with all information'),
            ('can_accept_applications', 'Can allow an applicant to become a member'),
            ('can_remove_member', 'Can remove a member from the club'),
            ('can_promote_member', 'Can promote a member to an officer'),
            ('can_demote_officer', 'Can demote an officer to a member'),
            ('can_transfer_ownership', 'Can transfer owner status to an officer'),
            ('can_become_owner', 'Can receive ownership of club'),
        ]
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

    def approve_applicant(self, user):
        """Change the group from applicant to member"""
        member = Group.objects.get(name = 'Member')
        member.user_set.add(user)

      
