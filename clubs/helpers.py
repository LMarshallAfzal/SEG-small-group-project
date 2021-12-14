# from django.conf import settings
# from django.shortcuts import redirect

# def login_prohibited(view_function):
#     def modified_view_function(request):
#         if request.user.is_authenticated:
#             return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
#         else:
#             return view_function(request)
#     return modified_view_function



# def owner_only(view_function):
#     def modified_view_function(request,*args, **kwargs):
#         current_user = request.user
#         if not (current_user.groups.filter(name='Owner').exists()):
#             if(current_user.groups.filter(name='Member').exists()):
#                 return redirect('member_list')
#             if(current_user.groups.filter(name='Applicant').exists()):
#                 return redirect('profile')
#             if(current_user.groups.filter(name='Officer').exists()):
#                 return redirect('officer_main')
#         else:
#             return view_function(request,*args, **kwargs)
#     return modified_view_function

# def officer_only(view_function):
#     def modified_view_function(request,*args, **kwargs):
#         current_user = request.user
#         if not (current_user.groups.filter(name='Officer').exists()):
#             if(current_user.groups.filter(name='Member').exists()):
#                 return redirect('member_list')
#             if(current_user.groups.filter(name='Applicant').exists()):
#                 return redirect('profile')
#             if(current_user.groups.filter(name='Owner').exists()):
#                 return redirect('owner')
#         else:
#             return view_function(request,*args, **kwargs)
#     return modified_view_function

# def member_only(view_function):
#     def modified_view_function(request,*args, **kwargs):
#         current_user = request.user
#         if not (current_user.groups.filter(name='Member').exists()):
#             if(current_user.groups.filter(name='Officer').exists()):
#                 return redirect('officer_main')
#             if(current_user.groups.filter(name='Applicant').exists()):
#                 return redirect('profile')
#             if(current_user.groups.filter(name='Owner').exists()):
#                 return redirect('owner_member_list')
#         else:
#             return view_function(request,*args, **kwargs)
#     return modified_view_function

def convert_to_codename(name):
    club_codename = ""
    #Removes whitespaces from the club name
    for character in name:
        if character == " ":
            club_codename += "_"
        else:
            club_codename += character
    return club_codename
