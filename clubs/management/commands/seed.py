from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Club
from django.db import IntegrityError
from faker import Faker
import faker.providers
import random
from django.contrib.auth.models import Group
import clubs.groups
from clubs.club_list import ClubList

class Command(BaseCommand):
    USER_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')


    def handle(self, *args, **options):
        list_of_clubs = ClubList()
        list_of_clubs.create_new_club("Kerbal Chess Club", self.faker.unique.text(max_nb_chars = 150), "Buckingham Palace")
        list_of_clubs.create_new_club("KCL Chess Society", self.faker.unique.text(max_nb_chars = 150), "Windsor Castle")
        list_of_clubs.create_new_club("UCL Terrible Chess Team", self.faker.unique.text(max_nb_chars = 150), "Drachenburg")
        list_of_clubs.create_new_club("Elite Cambridge Chess Team", self.faker.unique.text(max_nb_chars = 150), "Neuschwarnstein")


        Jebediah = User.objects.create_user(
            username = "jeb@example.org",
            first_name = "Jebediah",
            last_name = "Kerman",
            email = "jeb@example.org",
            password = "Password123",
            bio = self.faker.unique.text(max_nb_chars = 520),
            personal_statement = self.faker.text(max_nb_chars = 1250),
        )

        #TODO: Add failsafe for when the name is invalid
        club = list_of_clubs.find_club("Kerbal Chess Club")
        group = Group.objects.get(name = club.club_codename + " Member")
        Jebediah.groups.add(group)
        club.member_count += 1

        Valentina = User.objects.create_user(
            username = "val@example.org",
            first_name = "Valentina",
            last_name = "Kerman",
            email = "val@example.org",
            password = "Password123",
            bio = self.faker.unique.text(max_nb_chars = 520),
            personal_statement = self.faker.text(max_nb_chars = 1250),
        )
        group = Group.objects.get(name = list_of_clubs.find_club("Kerbal Chess Club").club_codename + " Officer")
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

        group = Group.objects.get(name = list_of_clubs.find_club("Kerbal Chess Club").club_codename + " Owner")
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

            #TODO: Make the group assignments for users realistic percentage + seed an owner for each club
            club = random.choice(list_of_clubs.club_list)
            group = Group.objects.get(name = club.club_codename + " " + random.choice(['Applicant', 'Member','Officer']))
            user.groups.add(group)

        for club in list_of_clubs.club_list:
            if club.club_name != "Kerbal Chess Club":
                club_users = User.objects.filter(groups__name__in = list_of_clubs.find_club(club.club_name).getGroupsForClub())
                new_owner = random.choice(club_users)
                new_owner.groups.clear()
                club.getClubOwnerGroup().user_set.add(new_owner)


        print('User seeding complete')

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email
