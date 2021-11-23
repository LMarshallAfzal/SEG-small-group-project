from .models import User
from django.shortcuts import render
from .forms import LogInForm, SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email = email, password = password)
            if user is not None:
                login(request, user)
                return redirect('member_list')
        #Add error message here
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})
    # if request.method == 'POST':
    #     form = LogInForm(request.POST)
    #     next = request.POST.get('next') or ''
    #     if form.is_valid():
    #         email = form.cleaned_data.get('email')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(email=email, password=password)
    #         if user is not None:
    #             login(request, user)
    #             redirect_url = next or 'feed'
    #             return redirect(redirect_url)
    #     messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    # else:
    #     next = request.GET.get('next') or ''
    # form = LogInForm()
    # return render(request, 'log_in.html', {'form': form, 'next': next})

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
    users = User.objects.all();
    return render(request, 'member_list.html', {'users': users})

def show_user(request, user_id):
    User = get_user_model()
    user = User.objects.get(id = user_id)
    return render(request, 'show_user.html', {'user' : user})

def officer_main(request):
    users = User.objects.all();
    return render(request, 'officer_main.html', {'users': users})
