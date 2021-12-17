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
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')


    def handle(self, *args, **options):
        #Seeds in clubs
        list_of_clubs = ClubList()
        list_of_clubs.create_new_club("Kerbal Chess Club", self.faker.unique.text(max_nb_chars = 150), "Buckingham Palace")
        list_of_clubs.create_new_club("KCL Chess Society", self.faker.unique.text(max_nb_chars = 150), "Windsor Castle")
        list_of_clubs.create_new_club("UCL Terrible Chess Team", self.faker.unique.text(max_nb_chars = 150), "Drachenburg")
        list_of_clubs.create_new_club("Elite Cambridge Chess Team", self.faker.unique.text(max_nb_chars = 150), "Neuschwarnstein")

        if not User.objects.filter(username='jeb@example.org').exists() or not User.objects.filter(username='val@example.org').exists() or not User.objects.filter(username='billie@example.org').exists():
            #Seeds in a member, officer and owner for the first club "Kerbal Chess Club"
            Jebediah = User.objects.create_user(
                username = "jeb@example.org",
                first_name = "Jebediah",
                last_name = "Kerman",
                email = "jeb@example.org",
                password = "Password123",
                experience_level = 'Beginner',
                bio = self.faker.unique.text(max_nb_chars = 520),
                personal_statement = self.faker.text(max_nb_chars = 1250),
            )
            Valentina = User.objects.create_user(
                username = "val@example.org",
                first_name = "Valentina",
                last_name = "Kerman",
                email = "val@example.org",
                password = "Password123",
                bio = self.faker.unique.text(max_nb_chars = 520),
                experience_level = "Intermediate",
                personal_statement = self.faker.text(max_nb_chars = 1250),
            )
            Billie = User.objects.create_user(
                username = "billie@example.org",
                first_name = "Billie",
                last_name = "Kerman",
                email = "billie@example.org",
                password = "Password123",
                experience_level = "Advanced",
                bio = self.faker.unique.text(max_nb_chars = 520),
                personal_statement = self.faker.text(max_nb_chars = 1250),
            )

            club = list_of_clubs.find_club("Kerbal Chess Club")
            group = Group.objects.get(name = club.club_codename + " Member")
            club.add_user_to_club(Jebediah, "Member")
            club = list_of_clubs.find_club("Kerbal Chess Club")
            group = Group.objects.get(name = club.club_codename + " Officer")
            club.add_user_to_club(Valentina, "Officer")
            club = list_of_clubs.find_club("Kerbal Chess Club")
            group = Group.objects.get(name = club.club_codename + " Owner")
            club.add_user_to_club(Billie, "Owner")

        #Creates a bucket of roles to choose from such that random.choice will choose approximately that percentage of each role
        applicant_percentage = 10
        member_percentage = 80
        officer_percentage = 10
        bucket = []
        for i in range(applicant_percentage + member_percentage + officer_percentage):
            if i < applicant_percentage:
                bucket.append("Applicant")
            elif i < applicant_percentage + member_percentage:
                bucket.append("Member")
            else:
                bucket.append("Officer")
        #Adds 250 users, split among clubs and non-owner roles within a club
        for _ in range(250):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = self._email(first_name, last_name)
            username = email
            password = "Password123"
            bio = self.faker.unique.text(max_nb_chars = 520)
            experience_level = random.choice(['Beginner', 'Intermediate', 'Advanced'])
            personal_statement = self.faker.text(max_nb_chars=1250)
            user = User.objects.create_user(
                username = username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
                bio = bio,
                personal_statement = personal_statement,
            )


            club = random.choice(list_of_clubs.club_list)
            role = random.choice(bucket)
            club.add_user_to_club(user, role)

        #Switches the role of a random user in each of the 3 extra clubs to owner
        for club in list_of_clubs.club_list:
            if club.club_name != "Kerbal Chess Club":
                club_users = User.objects.filter(groups__name__in = list_of_clubs.find_club(club.club_name).getGroupsForClub())
                new_owner = random.choice(club_users)
                club.switch_user_role_in_club(new_owner, "Owner")
        print('User seeding complete')

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email
