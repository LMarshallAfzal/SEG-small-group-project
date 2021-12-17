"""Contains a list of Club model instances as well as methods to act on Club model instances"""
from .groups import ChessClubGroups
from .models import Club, User

class ClubList:
    def __init__(self):
        self.club_list = []
        for club in Club.objects.all():
            self.club_list.append(club)

    def get_all_clubs(self):
        return self.club_list

    def find_club(self, club_name):
        for club in self.club_list:
            if club.club_name == club_name or club.club_codename == club_name:
                return club
        return None

    #Returns the club if the club was created successfully, None object if not
    def create_new_club(self, name, mission_statement, location):
        if self.find_club(name) == None:
            club = Club.objects.create_club(name, mission_statement, location)
            self.club_list.append(club)
            return club
        else:
            #Error message using None as return to keep UI elements in views.py?
            print("A club with that name already exists!")
            return None

    #Returns True if the club was deleted successfully, False if not
    def delete_club(self, club_name):
        club_to_delete = self.find_club(club_name)
        if club_to_delete == None:
            #Error message using False return to keep UI elements in views.py?
            #print("No club with that name exists!")
            return False
        else:
            self.club_list.remove(club_to_delete)
            club_to_delete.delete()
            return True

    #Returns 2D array in the form [[groups for a club][groups for a club]]
    def get_all_groups(self):
        all_groups = []
        for club in self.club_list:
            all_groups.append(club.getGroupsForClub())
        return all_groups

    #Gets the clubs the inputted user is a part of
    def get_user_clubs(self, user):
        user_clubs = []
        for club in self.club_list:
            if club.get_user_role_in_club(user) != None:
                user_clubs.append(club)
        return user_clubs
