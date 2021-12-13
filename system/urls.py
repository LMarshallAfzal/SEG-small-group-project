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
    path('log_in/', views.LogInView.as_view() , name = 'log_in'),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('log_out/', views.log_out, name = 'log_out'),
    path('show_current_user_profile/', views.show_current_user_profile, name = 'show_current_user_profile'),
    path('user/<int:user_id>', views.ShowUserView.as_view(), name='show_user'),
    path('officer_user/<int:user_id>', views.ShowOfficerView.as_view(), name='show_user_officer'),
    path('member_list/', views.MemberListView.as_view(), name = 'member_list'),
    path('officer/', views.officer, name = 'officer'),
    path('officer_promote_applicants/', views.ApplicantListView.as_view(), name = 'officer_promote_applicants'),
    path('officer_main/', views.OfficerMainListView.as_view(), name = 'officer_main'),
    path('reject_accept_handler/<int:user_id>', views.reject_accept_handler, name = 'officer_promote_applicants'),
    path('profile/',views.profile,name = 'profile'),
    path('password/', views.password, name='password'),
    path('owner/', views.owner, name = 'owner'),
    path('officer_list/', views.OfficerListView.as_view() ,name = 'officer_list'),
    path('owner_member_list', views.OwnerMemberListView.as_view(), name = 'owner_member_list'),
    path('promote_member/<int:user_id>', views.promote_member, name = 'promote_member'),
    path('demote_officer/<int:user_id>', views.demote_officer, name = 'demote_officer'),
    path('transfer_ownership/<int:user_id>', views.transfer_ownership, name = 'transfer_ownership'),
    path('club_selection/', views.club_selection, name = 'club_selection'),
    # path('club_dropdown/', views.club_dropdown, name = 'club_dropdown'),
    path('group_check/<int:user_id>', views.group_check, name = 'group_check'),
    path('application_form/', views.application_form, name = 'application_form'),
    path('create_new_club/', views.create_new_club, name = 'create_new_club')
]
