from .models import User
from django import template
from django.shortcuts import render
from .forms import LogInForm, SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.groups.filter(name = 'Officer'):
                    #user.groups.filter(name ='Member').exists()
                    login(request, user)

                    redirect_url = request.POST.get('next') or 'officer'
                    return redirect(redirect_url)
                    """View for member"""
                elif user.groups.filter(name = 'Member'):
                    pass
                    """View for owner"""
                elif user.groups.filter(name = 'Owner'):
                    pass
                    """View for applicant"""
                elif user.groups.filter(name = 'Applicant'):
                    pass
        #Add error message here
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    next = request.GET.get('next') or 'officer'
    return render(request, 'log_in.html', {'form': form, 'next' : next})

def log_out(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('member_list')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def member_list(request):
    users = User.objects.filter(groups__name = 'Member'); # This ensures only members on shown
    return render(request, 'member_list.html', {'users': users})

def show_user(request, user_id):
    User = get_user_model()
    user = User.objects.get(id = user_id)
    return render(request, 'show_user.html', {'user' : user})

def officer_main(request):
    users = User.objects.filter(groups__name__in=['Owner', 'Member', 'Officer'])
    groups = Group.objects.all()
    return render(request, 'officer_main.html', {'users': users})

def officer_promote_applicants(request):
    users = User.objects.filter(groups__name = 'Applicant');
    return render(request, 'officer_promote_applicants.html', {'users': users})

def officer(request):
    users = User.objects.all()
    return render(request, 'officer.html', {'users': users})

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
