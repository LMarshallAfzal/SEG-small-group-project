from typing import ContextManager, List

from django.views.generic.detail import DetailView
from .models import User
from django import template
from django.shortcuts import get_object_or_404, render
from .forms import LogInForm, SignUpForm, UserForm, PasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, Http404
from .models import User
from django.shortcuts import redirect, render
from .helpers import login_prohibited
from django.db.models import Count
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class LogInView(View):
    """Log-in handling view"""
    def get(self,request):
        self.next = request.GET.get('next') or 'officer'
        return self.render()

    def post(self,request):
        form = LogInForm(request.POST)
        self.next = request.GET.get('next') or 'officer'
        user = form.get_user()
        if user is not None:
                if user.groups.filter(name = 'Officer'):
                    #user.groups.filter(name ='Member').exists()
                    login(request, user)
                    redirect_url = request.POST.get('next') or 'officer'
                    return redirect(redirect_url)
                    """View for member"""
                elif user.groups.filter(name = 'Member'):
                    login(request, user)
                    #redirect_url = request.POST.get('next') or 'member_list'
                    return redirect('member_list')
                    #return redirect('show_current_user_profile')
                    """View for owner"""
                elif user.groups.filter(name = 'Owner'):
                    login(request, user)
                    return redirect('owner')
                    """View for applicant"""
                elif user.groups.filter(name = 'Applicant'):
                    login(request,user)
                    return redirect('show_current_user_profile')
        #Add error message here
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next' : self.next})


class MemberListView(LoginRequiredMixin,ListView):
    model = User
    template_name = 'member_list.html'
    context_object_name = 'users'

class OfficerListView(ListView):
    model = User
    template_name = 'officer_list.html'
    context_object_name = 'users'

class CurrentUserView(DetailView):
    model = User
    template_name = 'Żhow_current_user_profile.html'
    pk_url_kwarg = "user_id"

def show_user(request, user_id):
    User = get_user_model()
    user = User.objects.get(id = user_id)
    return render(request, 'show_user.html', {'user' : user})
    
@login_required
def show_user_officer(request, user_id):
    User = get_user_model()
    user = User.objects.get(id = user_id)
    return render(request, 'show_user_officer.html', {'user' : user})

def show_current_user_profile(request):
    current_user = request.user
    return render(request, 'show_current_user_profile.html', {'user': current_user})

@login_required
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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name = 'Applicant')
            user.groups.add(group)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            current_user.username = form.cleaned_data.get('email')
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('profile')#depends on the user type
    else:
        form = UserForm(instance=current_user)
    return render(request, 'profile.html', {'form': form})

@login_required
def password(request):
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.add_message(request, messages.SUCCESS, "Password updated!")
                return redirect('profile')
    form = PasswordForm()
    return render(request, 'password.html', {'form': form})




@login_required
def officer(request):
    users = User.objects.all()
    number_of_applicants = User.objects.filter(groups__name = 'Applicant').count()
    number_of_members = User.objects.filter(groups__name__in = ['Owner','Member','Officer']).count()
    return render(request, 'officer.html', {'users': users, 'number_of_applicants': number_of_applicants, 'number_of_members': number_of_members})

@login_required
def officer_main(request):
    users = User.objects.filter(groups__name__in=['Owner', 'Member', 'Officer'])
    groups = Group.objects.all()
    return render(request, 'officer_main.html', {'users': users})

@login_required
def officer_promote_applicants(request):
    users = User.objects.filter(groups__name = 'Applicant')
    return render(request, 'officer_promote_applicants.html', {'users': users})

def reject_accept_handler(request, user_id):
    if request.POST:
        if 'accept' in request.POST:
            accept(request, user_id)
        elif 'reject' in request.POST:
            reject(request, user_id)
    return redirect('officer_promote_applicants')

def accept(request, user_id):
    User = get_user_model()
    user = User.objects.get(id = user_id)
    member = Group.objects.get(name = 'Member')
    member.user_set.add(user)
    applicant = Group.objects.get(name = 'Applicant')
    applicant.user_set.remove(user)
    #return redirect('officer_main')

def reject(request, user_id):
    User = get_user_model()
    user = User.objects.get(id = user_id)
    user.delete()
    #return redirect('officer_main')

@login_required
def owner(request):
    users = User.objects.all()
    number_of_applicants = User.objects.filter(groups__name = 'Applicant').count()
    number_of_members = User.objects.filter(groups__name__in = ['Owner','Member']).count()
    number_of_officers = User.objects.filter(groups__name = 'Officer').count()
    return render(request, 'owner.html', {'users': users, 'number_of_applicants': number_of_applicants, 'number_of_members': number_of_members, 'number_of_officers': number_of_officers})

@login_required
def officer_list(request):
    users = User.objects.filter(groups__name = 'Officer')
    groups = Group.objects.all()
    return render(request, 'officer_list.html', {'users': users})

@login_required
def owner_member_list(request):
    users = User.objects.filter(groups__name = 'Member')
    groups = Group.objects.all()
    return render(request, 'owner_member_list.html', {'users': users})

@login_required
def transfer_ownership(request, user_id):
    user = get_user_model()
    user = User.objects.get(id = user_id)
    officer = Group.objects.get(name = "Officer")
    owner = Group.objects.get(name = "Owner")
    current_owner = User.objects.get(username = request.user.get_username())
    owner.user_set.add(user)
    owner.user_set.remove(current_owner)
    officer.user_set.add(current_owner)
    officer.user_set.remove(user)
    logout(request)
    return redirect('home')
    # else:
    #     messages.add_message(request, messages.ERROR, "New owner has to be an officer!")
    #     return redirect('show_user')

@login_required
def promote_member(request, user_id):
    user = get_user_model()
    user = User.objects.get(id = user_id)
    officer = Group.objects.get(name = "Officer")
    officer.user_set.add(user)
    member = Group.objects.get(name = 'Member')
    member.user_set.remove(user)
    return redirect('owner_member_list')

@login_required
def demote_officer(request, user_id):
    user = get_user_model()
    user = User.objects.get(id = user_id)
    officer = Group.objects.get(name = "Officer")
    officer.user_set.remove(user)
    member = Group.objects.get(name = 'Member')
    member.user_set.add(user)
    return redirect('officer_list')
