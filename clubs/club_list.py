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

    #TODO: What else happens when a club is deleted? (e.g: Changes to database etc)
    def delete_club(club_name):
        club_to_delete = find_club(club_name)
        if club_to_delete == None:
            #Error message
            print("No club with that name exists!")
        else:
            club_list.remove(club_to_delete)
            #Complete deletion process



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

    def getGroupsForClub(self):
        return [self.club_groups_and_permissions.applicant_group, self.club_groups_and_permissions.member_group, self.club_groups_and_permissions.officer_group, self.club_groups_and_permissions.owner_group]

    def getClubApplicantGroup(self):
        return self.club_groups_and_permissions.applicant_group

    def getClubMemberGroup(self):
        return self.club_groups_and_permissions.member_group

    def getClubOfficerGroup(self):
        return self.club_groups_and_permissions.officer_group

    def getClubOwnerGroup(self):
        return self.club_groups_and_permissions.owner_group
