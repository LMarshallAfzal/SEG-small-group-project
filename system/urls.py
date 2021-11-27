"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clubs import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('log_in/', views.log_in, name = 'log_in'),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('log_out/', views.log_out, name = 'log_out'),
    path('show_current_user_profile/', views.show_current_user_profile, name = 'show_current_user_profile'),
    path('user/<int:user_id>', views.show_user, name='show_user'),
    path('member_list/', views.member_list, name = 'member_list'),
    path('officer/', views.officer, name = 'officer'),
    path('officer_promote_applicants/', views.officer_promote_applicants, name = 'officer_promote_applicants'),
    path('officer_main/', views.officer_main, name = 'officer_main'),
    path('user/<int:user_id>', views.reject_accept_handler, name = 'officer_main'),
]
