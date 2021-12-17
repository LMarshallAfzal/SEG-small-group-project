from typing import List
from django import template
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import LogInForm, SignUpForm, UserForm, PasswordForm, ApplicationForm, CreateClubForm
from django.template import RequestContext
#from django.core.context_processors import csrf
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, Http404
from .models import User
from django.shortcuts import redirect, render
    # from .helpers import login_prohibited,owner_only ,officer_only, member_only
from django.db.models import Count
from django.views import View
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .club_list import ClubList
from django.core.paginator import Paginator
from django.conf import settings
from django.urls import reverse
from .models import User
from django.shortcuts import render, redirect
from .forms import LogInForm, SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def getClubAndListOfClubsWithObjectParameter(obj):
    list_of_clubs = ClubList()
    name_of_club = obj.request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    return club, list_of_clubs

def getClubAndListOfClubs(request):
    list_of_clubs = ClubList()
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    return club, list_of_clubs


class LoginProhibitedMixin:

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('club_selection')

        return super().dispatch(*args, **kwargs)



class MemberOnlyMixin:

    def dispatch(self, *args, **kwargs):
        current_user = self.request.user
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        if not (current_user.groups.filter(name = club.getClubMemberGroup()).exists() or current_user.groups.filter(name = club.getClubOfficerGroup()).exists() or current_user.groups.filter(name = club.getClubOwnerGroup()).exists()):
            return redirect('profile')
        return super().dispatch(*args, **kwargs)



class OfficerOnlyMixin:

    def dispatch(self, *args, **kwargs):
        current_user = self.request.user
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        if not (current_user.groups.filter(name = club.getClubOfficerGroup()).exists() or current_user.groups.filter(name = club.getClubOwnerGroup()).exists()):
            return redirect('profile')
        return super().dispatch(*args, **kwargs)


class OwnerOnlyMixin:

    def dispatch(self, *args, **kwargs):
        current_user = self.request.user
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        if not (current_user.groups.filter(name = club.getClubOwnerGroup()).exists()):
            return redirect('profile')
        return super().dispatch(*args, **kwargs)


class LogInView(LoginProhibitedMixin,View):
    """Log-in handling view"""
    def get(self,request):
        self.next = request.GET.get('next') or 'officer'
        return self.render()

    def post(self,request):
        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or 'officer'
        user = form.get_user()
        if user is not None:
                """Redirect to club selection page, with option to create new club"""
                login(request, user)
                return redirect('club_selection')

        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next' : self.next})


class MemberListView(LoginRequiredMixin,MemberOnlyMixin,ListView):
    model = User
    template_name = 'member_list.html'
    context_object_name = 'users'
    #paginate_by = settings.USERS_PER_PAGE

    def get_queryset(self):
          qs = super().get_queryset()
          club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
          return qs.filter(groups__name__in=[club.getClubApplicantGroup(),club.getClubOwnerGroup(), club.getClubMemberGroup(), club.getClubOfficerGroup()])

    def get(self,request,*args, **kwargs):
        # list_of_clubs = ClubList()
        # name_of_club = self.request.session.get('club_name')
        # club = list_of_clubs.find_club(name_of_club)
        # queryset = User.objects.filter(groups__name=club.getClubMemberGroup())
        # users = queryset
        return self.render()

    def post(self,request,*args, **kwargs):
        # list_of_clubs = ClubList()
        # name_of_club = self.request.session.get('club_name')
        # club = list_of_clubs.find_club(name_of_club)
        # queryset = User.objects.filter(groups__name=club.getClubMemberGroup())
        # users = queryset
        return self.redirect('club_selection')

    def render(self):
        qs = super().get_queryset()
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        clubs = list_of_clubs.club_list
        users = qs.filter(groups__name__in=[club.getClubMemberGroup()])
        return render(self.request, 'member_list.html', {'users':users, 'clubs':clubs})



class OfficerMainListView(OfficerOnlyMixin,MemberListView):
    template_name = 'officer_main.html'


    def get_context_data(self, *args, **kwargs):
        """Generate content to be displayed in the template."""
        context = super().get_context_data(*args, **kwargs)
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        context['number_of_applicants'] = User.objects.filter(groups__name = club.getClubApplicantGroup()).count()
        context['number_of_members'] = User.objects.filter(groups__name__in = [club.getClubOwnerGroup(),club.getClubMemberGroup(), club.getClubOfficerGroup()]).count()
        return context

    def get(self,request,*args, **kwargs):
        # list_of_clubs = ClubList()
        # name_of_club = self.request.session.get('club_name')
        # club = list_of_clubs.find_club(name_of_club)
        # queryset = User.objects.filter(groups__name=club.getClubMemberGroup())
        # users = queryset
        return self.render()



    def post(self,request,*args, **kwargs):
        # list_of_clubs = ClubList()
        # name_of_club = self.request.session.get('club_name')
        # club = list_of_clubs.find_club(name_of_club)
        # queryset = User.objects.filter(groups__name=club.getClubMemberGroup())
        # users = queryset
        return self.render()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def render(self):
        qs = super().get_queryset()
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        clubs = list_of_clubs.club_list
        users = qs.filter(groups__name__in=[club.getClubMemberGroup()])
        return render(self.request, 'officer_main.html', {'users':users, 'clubs':clubs})


# class OwnerMemberListView(OfficerMainListView):

#     template_name = 'owner_member_list.html'
#     # paginate_by = settings.USERS_PER_PAGE




class OwnerMemberListView(OwnerOnlyMixin,MemberListView):
    template_name = 'owner_member_list.html'
    context_object_name = 'users'
    # paginate_by = settings.USERS_PER_PAGE

    def get_context_data(self, *args, **kwargs):
        """Generate content to be displayed in the template."""
        context = super().get_context_data(*args, **kwargs)
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        context['number_of_applicants'] = User.objects.filter(groups__name = club.getClubApplicantGroup()).count()
        context['number_of_members'] = User.objects.filter(groups__name__in = [club.getClubOwnerGroup(),club.getClubMemberGroup(), club.getClubOfficerGroup()]).count()
        return context

    def get(self,request,*args, **kwargs):
        # list_of_clubs = ClubList()
        # name_of_club = self.request.session.get('club_name')
        # club = list_of_clubs.find_club(name_of_club)
        # queryset = User.objects.filter(groups__name=club.getClubMemberGroup())
        # users = queryset
        return self.render()



    def post(self,request,*args, **kwargs):
        # list_of_clubs = ClubList()
        # name_of_club = self.request.session.get('club_name')
        # club = list_of_clubs.find_club(name_of_club)
        # queryset = User.objects.filter(groups__name=club.getClubMemberGroup())
        # users = queryset
        return self.render()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def render(self):
        qs = super().get_queryset()
        clubs = list_of_clubs.club_list
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        users = qs.filter(groups__name__in=[club.getClubMemberGroup()])
        return render(self.request, 'owner_member_list.html', {'users':users, 'clubs':clubs})

class OfficerListView(OwnerMemberListView):

    template_name = 'officer_list.html'

    def render(self):
        qs = super().get_queryset()
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        clubs = list_of_clubs.club_list
        users = qs.filter(groups__name__in=[club.getClubOfficerGroup()])
        return render(self.request, 'officer_list.html', {'users':users, 'clubs':clubs})


class ApplicantListView(OfficerMainListView):
    template_name = 'officer_promote_applicants.html'

    def render(self):
        qs = super().get_queryset()
        list_of_clubs = ClubList()
        name_of_club = self.request.session.get('club_name')
        club = list_of_clubs.find_club(name_of_club)
        clubs = list_of_clubs.club_list
        users = qs.filter(groups__name__in=[club.getClubApplicantGroup()])
        return render(self.request, 'officer_promote_applicants.html', {'users':users, 'clubs': clubs})


class ShowUserView(DetailView):
    model = User
    template_name = 'show_user.html'
    pk_url_kwarg = "user_id"



class ShowOfficerView(OfficerOnlyMixin,DetailView):
    model = User
    template_name = 'show_user_officer.html'
    pk_url_kwarg = "user_id"
    list_of_clubs = ClubList()
    clubs = list_of_clubs.club_list


class SignUpView(LoginProhibitedMixin,FormView):

    form_class = SignUpForm
    template_name = "sign_up.html"

    def form_valid(self, form):
        self.object = form.save()
        login(self.request,self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('club_selection')

class OwnerView(OwnerMemberListView):

    template_name = 'owner.html'

    def render(self):
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        clubs = list_of_clubs.club_list
        users = User.objects.all()
        number_of_applicants = User.objects.filter(groups__name = club.getClubApplicantGroup()).count()
        number_of_members = User.objects.filter(groups__name__in = [ club.getClubOwnerGroup(), club.getClubMemberGroup()]).count()
        number_of_officers = User.objects.filter(groups__name = club.getClubOfficerGroup()).count()
        return render(self.request, 'owner.html', {'users': users, 'number_of_applicants': number_of_applicants, 'number_of_members': number_of_members, 'number_of_officers': number_of_officers, 'clubs': clubs})

class OfficerView(OfficerMainListView):

    template_name = 'officer.html'

    def render(self):
        club, list_of_clubs = getClubAndListOfClubsWithObjectParameter(self)
        clubs = list_of_clubs.club_list
        users = User.objects.all()
        number_of_applicants = User.objects.filter(groups__name = club.getClubApplicantGroup()).count()
        number_of_members = User.objects.filter(groups__name__in = [ club.getClubOwnerGroup(), club.getClubMemberGroup()]).count()
        number_of_officers = User.objects.filter(groups__name = club.getClubOfficerGroup()).count()
        return render(self.request, 'officer.html', {'users': users, 'number_of_applicants': number_of_applicants, 'number_of_members': number_of_members, 'number_of_officers': number_of_officers, 'clubs' : clubs})



class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        return self.render()

    def post(self,request):
        current_user = request.user
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            current_user.username = form.cleaned_data.get('email')
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
        return redirect('profile')#depends on the user type

    def render(self):
        current_user = self.request.user
        form = UserForm(instance=current_user)
        return render(self.request,'profile.html', {'form': form})




def show_current_user_profile(request):
    list_of_clubs = ClubList()
    clubs = list_of_clubs.club_list
    current_user = request.user
    return render(request, 'show_current_user_profile.html', {'user': current_user, 'clubs':clubs})


def group_check(request):
    list_of_clubs = ClubList()
    clubs = list_of_clubs.club_list
    request.session['club_name'] = request.POST.get('club_name')
    name_of_club = request.session.get('club_name')
    club = list_of_clubs.find_club(name_of_club)
    print(request.POST.get('club_name'))
    user = request.user
    group_role = club.get_user_role_in_club(user)
    if group_role == "Officer":
        #user.groups.filter(name ='Member').exists()
        redirect_url = request.POST.get('next') or 'officer'
        return redirect(redirect_url)
        """View for member"""
    elif group_role == "Member":
        #redirect_url = request.POST.get('next') or 'member_list'
        return redirect('member_list')
        #return redirect('show_current_user_profile')
        """View for owner"""
    elif group_role == "Owner":
        return redirect('owner')
        """View for applicant"""
    elif group_role == "Applicant":
        return redirect('show_current_user_profile')
    else:
        return redirect('application_form')

def log_out(request):
    logout(request)
    return redirect('home')

class HomeView(LoginProhibitedMixin,View):
    template_name = 'home.html'

    def get(self,request):
        return self.render()

    def post(self,request):
        return self.render()

    def render(self):
        return render(self.request, 'home.html')


def application_form(request):
    club, list_of_clubs = getClubAndListOfClubs(request)
    clubs = list_of_clubs.club_list
    current_user = request.user
    if request.method == 'POST':
        form = ApplicationForm(instance=current_user, data = request.POST)
        #form.instance = current_user
        if form.is_valid():
            current_user.username = form.cleaned_data.get('email')
            club.add_user_to_club(current_user, "Applicant")
            messages.add_message(request, messages.SUCCESS, "You have joined a new club!")
            form.save()
            return redirect('profile')
    else:
        form = ApplicationForm(instance=current_user)
    return render(request, 'application_form.html', {'form': form, 'clubs':clubs})

class PasswordView(LoginRequiredMixin, FormView):
    """View that handles password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('profile')

def reject_accept_handler(request, user_id):
    if request.POST:
        if 'accept' in request.POST:
            accept(request, user_id)
        elif 'reject' in request.POST:
            reject(request, user_id)
    return redirect('officer_promote_applicants')


def accept(request, user_id):
    club, list_of_clubs = getClubAndListOfClubs(request)
    clubs = list_of_clubs.club_list
    User = get_user_model()
    user = User.objects.get(id = user_id)
    club.switch_user_role_in_club(user, "Member")

def reject(request, user_id):
    User = get_user_model()
    user = User.objects.get(id = user_id)
    user.delete()



def transfer_ownership(request, user_id):
    club, list_of_clubs = getClubAndListOfClubs(request)
    user = get_user_model()
    user = User.objects.get(id = user_id)
    current_owner = User.objects.get(username = request.user.get_username())
    club.switch_user_role_in_club(user, "Owner")
    club.switch_user_role_in_club(current_owner, "Officer")
    logout(request)
    return  redirect('owner')



def promote_member(request, user_id):
    club, list_of_clubs = getClubAndListOfClubs(request)
    user = get_user_model()
    user = User.objects.get(id = user_id)
    club.switch_user_role_in_club(user, "Officer")
    return redirect('owner_member_list')


def promoteOfficer(request,user_id):
    club, list_of_clubs = getClubAndListOfClubs(request)
    user = get_user_model()
    user = User.objects.get(id = user_id)
    officer = Group.objects.get(name = club.getClubOfficerGroup())
    officer.user_set.add(user)
    member = Group.objects.get(name = club.getClubMemberGroup())
    member.user_set.remove(user)
    return redirect('owner_member_list')

def demote_officer(request, user_id):
    club, list_of_clubs = getClubAndListOfClubs(request)
    user = get_user_model()
    user = User.objects.get(id = user_id)
    club.switch_user_role_in_club(user, "Member")
    return redirect('officer_list')



def club_selection(request):
    list_of_clubs = ClubList()
    clubs = list_of_clubs.club_list
    owners = []
    member_count_list = []
    for club in clubs:
        owners.append(club.get_club_owner())
        member_count_list.append(User.objects.filter(groups__name__in = [club.getClubOwnerGroup(), club.getClubMemberGroup(), club.getClubOfficerGroup()]).count())
    clubs_and_owners = zip(clubs, owners, member_count_list)
    return render(request, 'club_selection.html', {'clubs_and_owners' : clubs_and_owners, 'clubs':clubs, 'member_count_list':member_count_list})



def create_new_club(request):
    list_of_clubs = ClubList()
    clubs = list_of_clubs.club_list
    user = request.user
    if request.method == 'POST':
        form = CreateClubForm(data = request.POST)
        if form.is_valid():

            list_of_clubs = ClubList()
            list_of_clubs.create_new_club(
                form.cleaned_data.get('club_name'),
                form.cleaned_data.get('mission_statement'),
                form.cleaned_data.get('club_location')
            )
            club = list_of_clubs.find_club(form.cleaned_data.get('club_name'))
            club.add_user_to_club(user, "Owner")
            messages.add_message(request, messages.SUCCESS, "You have created a new chess club!")
            return redirect('club_selection')
    else:
        form = CreateClubForm()
    return render(request, 'new_club_form.html', {'form': form})

def delete_club(request):
    list_of_clubs = ClubList()
    name_of_club = request.session.get('club_name')
    user = request.user
    if request.method == 'POST':
        club = list_of_clubs.find_club(name_of_club)
        for group in club.getGroupsForClub():
            Group.objects.filter(name=group).delete()
        list_of_clubs.delete_club(name_of_club)
        messages.add_message(request, messages.SUCCESS, "You have deleted a chess club!")
        return redirect('club_selection')

