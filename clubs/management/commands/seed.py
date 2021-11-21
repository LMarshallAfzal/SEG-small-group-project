from django.core.management.base import BaseCommand, CommandError
from clubs.models import User
from django.db import IntegrityError
from faker import Faker
import faker.providers

class Command(BaseCommand):
    USER_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        # user_count = 0
        # while user_count < Command.USER_COUNT:
        #     print(f'Seeding user {user_count}',  end='\r')
        #     try:
        #         self._create_user()
        #     except (django.db.utils.IntegrityError):
        #         continue
        #     user_count += 1
        for _ in range(100):
            firstName = self.faker.unique.first_name()
            lastName = self.faker.unique.last_name()
            userName = firstName
            email1 = self._email(firstName, lastName)
            pass1 = self.faker.unique.password()
            bio1 = self.faker.unique.text(max_nb_chars = 520)
            personalStatement = self.faker.text(max_nb_chars=1250)

            User.objects.create_user(
                username = userName,
                first_name = firstName,
                last_name = lastName, 
                email = email1,
                password = pass1,
                bio = bio1,
                personal_statement = personalStatement,
                )
        print('User seeding complete')

    # def _create_user(self):
    #     first_name = self.faker.first_name()
    #     last_name = self.faker.last_name()
    #     email = self._email(first_name, last_name)
    #     password = self.faker.unique.password()
    #     bio = self.faker.text(max_nb_chars=520)
    #     personal_statement = self.faker.text(max_nb_chars=1250)
    #     User.objects.create_user(
    #         username = first_name,
    #         first_name=first_name,
    #         last_name=last_name,
    #         email=email,
    #         password=password,
    #         bio=bio,
    #         personal_statement=personal_statement,
    #
    #
    #     )

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email
