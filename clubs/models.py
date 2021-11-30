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
