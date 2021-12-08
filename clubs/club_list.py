"""Contains a list of Club model instances as well as methods to act on Club model instances"""
from .groups import ChessClubGroups
from .models import Club


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

    def create_new_club(self, name):
        if self.find_club(name) == None:
            club = Club.objects.create_club(name)
            self.club_list.append(club)
        else:
            #Error message
            print("A club with that name already exists!")

    #TODO: What else happens when a club is deleted? (e.g: Changes to database etc)
    def delete_club(self, club_name):
        club_to_delete = self.find_club(club_name)
        if club_to_delete == None:
            #Error message
            print("No club with that name exists!")
        else:
            club.delete()
            #Complete deletion process

    #Returns 2D array in the form [[groups for a club][groups for a club]]
    def get_all_groups(self):
        all_groups = []
        for club in self.club_list:
            all_groups.append(club.getGroupsForClub())
        return all_groups
