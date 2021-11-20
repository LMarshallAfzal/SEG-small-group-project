from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
    #Note: AbstractUser contains a required username field by default,
    #therefore every User must have a username.
    #No username field specification = uses default implementation.
    first_name = models.CharField(max_length = 50, blank = False)
    last_name = models.CharField(max_length = 50, blank = False)
    email = models.EmailField(unique = True, blank = False)
    bio = models.CharField(max_length = 520, blank = False)
    EXPERIENCE_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]
    experience_level = models.CharField(max_length = 12, choices = EXPERIENCE_CHOICES, default = BEGINNER)
    personal_statement = models.CharField(max_length = 1250, blank = False)



# Create your models here.
