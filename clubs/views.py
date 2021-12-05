from typing import List
from django import template
from django.shortcuts import render
from django.template import RequestContext
from .forms import LogInForm, SignUpForm, UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from .models import User, Club
from django.shortcuts import redirect, render
from .helpers import login_prohibited
from django.db.models import Count
from .club_list import ClubList

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                # user_groups = []
                # for group in user.groups.all():
                #     user_groups.append(group.name)
                #
                # user_clubs = []
                #gets the club that a user is a part of
                # for club in ClubList.club_list:
                #     club_groups = club.getGroupsForClub()
                #     for group in club_groups:
                #         if group in user_groups:
                #             user_clubs.append(club)

                #Find a way of redirecting correct users to the club club_selection
                #Ensure that they only can see clubs they are a part of
                #When they access a club make sure they have correct peremissions (applicant, member, officer, owner)

                """Redirect to club selection page, with option to create new club"""
                login(request, user)
                return redirect('club_selection')

        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    next = request.GET.get('next') or 'officer'
    return render(request, 'log_in.html', {'form': form, 'next' : next})

def group_check(request, user_id):
    list_of_clubs = ClubList()
    request.session['club_name'] = request.POST.get('club_name')
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    print(request.POST.get('club_name'))
    user = User.objects.get(id = user_id)
    if user.groups.filter(name = club.getClubOfficerGroup()):
        #user.groups.filter(name ='Member').exists()
        redirect_url = request.POST.get('next') or 'officer'
        return redirect(redirect_url)
        """View for member"""
    elif user.groups.filter(name =  club.getClubMemberGroup()):
        #redirect_url = request.POST.get('next') or 'member_list'
        return redirect('member_list')
        #return redirect('show_current_user_profile')
        """View for owner"""
    elif user.groups.filter(name = club.getClubOwnerGroup()):
        pass
        """View for applicant"""
    elif user.groups.filter(name = club.getClubApplicantGroup()):
        pass
    else:
        return redirect('club_selection')

def log_out(request):
    logout(request)
    return redirect('home')

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_required
def show_current_user_profile(request):
    current_user = request.user
    return render(request, 'show_current_user_profile.html', {'user': current_user})

@login_prohibited
def sign_up(request):
    list_of_clubs = ClubList()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            club = list_of_clubs.find_club(user.clubs)
            group = Group.objects.get(name = club.getClubApplicantGroup())
            user.groups.add(group)
            login(request, user)
            return redirect('club_selection')#should be an applicant page
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('profile')#depends on the user type
    else:
        form = UserForm(instance=current_user)
    return render(request, 'profile.html', {'form': form})

@login_required
def member_list(request):
    list_of_clubs = ClubList()
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    users = User.objects.filter(groups__name__in=[club.getClubOwnerGroup(), club.getClubMemberGroup(), club.getClubOfficerGroup()])
    return render(request, 'member_list.html', {'users': users})

@login_required
def show_user(request, user_id):
    User = get_user_model()
    user = User.objects.get(id = user_id)
    return render(request, 'show_user.html', {'user' : user})

@login_required
def show_user_officer(request, user_id):
    User = get_user_model()
    user = User.objects.get(id = user_id)
    return render(request, 'show_user_officer.html', {'user' : user})

@login_required
def officer(request):
    list_of_clubs = ClubList()
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    users = User.objects.all()
    number_of_applicants = User.objects.filter(groups__name = club.getClubApplicantGroup()).count()
    number_of_members = User.objects.filter(groups__name__in = [club.getClubOwnerGroup(),club.getClubMemberGroup(),club.getClubOfficerGroup()]).count()
    return render(request, 'officer.html', {'users': users, 'number_of_applicants': number_of_applicants, 'number_of_members': number_of_members})

@login_required
def officer_main(request):
    list_of_clubs = ClubList()
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    users = User.objects.filter(groups__name__in=[club.getClubOwnerGroup(), club.getClubMemberGroup(), club.getClubOfficerGroup()])
    groups = Group.objects.all()
    return render(request, 'officer_main.html', {'users': users})

@login_required
def officer_promote_applicants(request):
    list_of_clubs = ClubList()
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    users = User.objects.filter(groups__name = club.getClubApplicantGroup());
    return render(request, 'officer_promote_applicants.html', {'users': users})

def reject_accept_handler(request, user_id):
    if request.POST:
        if 'accept' in request.POST:
            accept(request, user_id)
        elif 'reject' in request.POST:
            reject(request, user_id)
    return redirect('officer_promote_applicants')

def accept(request, user_id):
    list_of_clubs = ClubList()
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    User = get_user_model()
    user = User.objects.get(id = user_id)
    member = Group.objects.get(name = club.getClubMemberGroup())
    member.user_set.add(user)
    applicant = Group.objects.get(name = club.getClubApplicantGroup())
    applicant.user_set.remove(user)

def reject(request, user_id):
    User = get_user_model()
    user = User.objects.get(id = user_id)
    user.delete()
    #return redirect('officer_main')

@login_required
def newOwner(request,user_id):
    list_of_clubs = ClubList()
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    user = get_user_model()
    user = User.objects.get(id = user_id)
    officer = Group.objects.get(name = club.getClubOfficerGroup)
    if user in officer.user_set:
        owner = Group.objects.get(name = club.getClubOwnerGroup())
        owners = List(Group.objects.getAll(name = club.getClubOwnerGroup()))
        current_owner = owners[0]
        owner.user_set.add(user)
        owner.user_set.remove(current_owner)
        logout(request)
        return redirect('home')

    else:
        messages.add_message(request, messages.ERROR, "New owner has to be an officer!")
        return redirect('show_user')

@login_required
def promoteOfficer(request,user_id):
    ist_of_clubs = ClubList()
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    user = get_user_model()
    user = User.objects.get(id = user_id)
    officer = Group.objects.get(name = club.getClubOfficerGroup)
    officer.user_set.add(user)
    return redirect('show_user')

@login_required
def demoteOfficer(request,user_id):
    user = get_user_model()
    user = User.objects.get(id = user_id)
    officer = Group.objects.get(name = club.getClubOfficerGroup())
    officer.user_set.remove(user)
    return redirect('show_user')

def club_selection(request):
    list_of_clubs = ClubList()
    clubs = list_of_clubs.club_list
    print(len(clubs))
    return render(request, 'club_selection.html', {'clubs':clubs})
