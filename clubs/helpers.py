from django.conf import settings
from django.shortcuts import redirect

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
