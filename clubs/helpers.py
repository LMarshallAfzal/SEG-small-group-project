from django.conf import settings
from django.shortcuts import redirect
from clubs.models import User, Club

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def convert_to_codename(name):
    club_codename = ""
    #Removes whitespaces from the club name
    for character in name:
        if character == " ":
            club_codename += "_"
        else:
            club_codename += character
    return club_codename

#Gets the role of the user in a specific club (roles correspond to groups)
def get_user_role_in_club(user, club):
    if user.groups.filter(name = club.club_codename + " Applicant").exists():
        return "Applicant"
    elif user.groups.filter(name = club.club_codename + " Member").exists():
        return "Member"
    elif user.groups.filter(name = club.club_codename + " Officer").exists():
        return "Officer"
    elif user.groups.filter(name = club.club_codename + " Owner").exists():
        return "Owner"
    else:
        return None #If the user is not part of the club this will be returned
