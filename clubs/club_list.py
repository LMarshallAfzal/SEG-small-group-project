"""Clubs are defined + methods to filter a club etc (finish description once done)"""
from clubs.groups import ChessClubGroups


class ClubList:
    club_list = [] #This class variable will track all clubs.

    def find_club(club_name):
        for club in club_list:
            if club.club_name == club_name or club.club_codename == club_name:
                return club
        return None

    def create_new_club(club_name):
        if find_club(club_name) != None:
            club_list.append(Club(club_name))
        else:
            #Error message
            print("A club with that name already exists!")



class Club:
    def __init__(self, club_name):
        self.club_name = club_name
        self.club_codename = ""
        #Removes whitespaces from the club name
        for character in club_name:
            if character == " ":
                self.club_codename += "_"
            else:
                self.club_codename += character
        self.club_groups_and_permissions = ChessClubGroups(self.club_codename)

    def get_club_groups_as_list(self):
        pass
