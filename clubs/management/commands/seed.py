from django.core.management.base import BaseCommand, CommandError
from clubs.models import User
from django.db import IntegrityError
from faker import Faker
import faker.providers
import random
from django.contrib.auth.models import Group
import clubs.groups

class Command(BaseCommand):
    USER_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        Jebediah = User.objects.create_user(
            username = "jeb@example.org",
            first_name = "Jebediah",
            last_name = "Kerman",
            email = "jeb@example.org",
            password = "Password123",
            bio = self.faker.unique.text(max_nb_chars = 520),
            personal_statement = self.faker.text(max_nb_chars = 1250),
        )

        group = Group.objects.get(name = 'Member')
        Jebediah.groups.add(group)

        Valentina = User.objects.create_user(
            username = "val@example.org",
            first_name = "Valentina",
            last_name = "Kerman",
            email = "val@example.org",
            password = "Password123",
            bio = self.faker.unique.text(max_nb_chars = 520),
            personal_statement = self.faker.text(max_nb_chars = 1250),
        )

        group = Group.objects.get(name = 'Officer')
        Valentina.groups.add(group)

        Billie = User.objects.create_user(
            username = "billie@example.org",
            first_name = "Billie",
            last_name = "Kerman",
            email = "billie@example.org",
            password = "Password123",
            bio = self.faker.unique.text(max_nb_chars = 520),
            personal_statement = self.faker.text(max_nb_chars = 1250),
        )

        group = Group.objects.get(name = 'Owner')
        Billie.groups.add(group)


        for _ in range(100):
            firstName = self.faker.unique.first_name()
            lastName = self.faker.unique.last_name()
            email1 = self._email(firstName, lastName)
            userName = email1
            pass1 = "Password123"
            bio1 = self.faker.unique.text(max_nb_chars = 520)
            personalStatement = self.faker.text(max_nb_chars=1250)

            user = User.objects.create_user(
                username = userName,
                first_name = firstName,
                last_name = lastName,
                email = email1,
                password = pass1,
                bio = bio1,
                personal_statement = personalStatement,
            )
            
            #TODO: Make the group assignments for users realistic percentage
            group = Group.objects.get(name = random.choice(['Applicant', 'Member','Officer']))
            user.groups.add(group)

        print('User seeding complete')

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email
