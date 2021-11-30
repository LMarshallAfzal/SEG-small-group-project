"""Creates groups and assigns permissions for the groups for a chess club"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from clubs.models import User

#Stores a list of all the ChessClubGroups objects: this can be used to access the groups for each club.
club_list = []

#The club name is passed in to be used as a way of separating groups and permissions for each club
class ChessClubGroups(temp_chess_club_name):
    #Club name will have no whitespaces for the permission code
    chess_club_name = ""
    for character in chess_club_name:
        if character == " ":
            chess_club_name += "_"
        else:
            chess_club_name += character

    #Creates groups for each chess club
    applicant_group, created = Group.objects.get_or_create(name = chess_club_name + ' Applicant')
    member_group, created = Group.objects.get_or_create(name = chess_club_name + ' Member')
    officer_group, created = Group.objects.get_or_create(name = chess_club_name + ' Officer')
    owner_group, created = Group.objects.get_or_create(name = chess_club_name + ' Owner')

    user_content_type = ContentType.objects.get_for_model(User)

    #Creates permissions for each club and assigns permissions to groups.

    member_list_permission = Permission.objects.create(
        codename = 'can_access_member_list_' + chess_club_name,
        name = 'Can access a basic list of members and some details for club ' + chess_club_name,
        content_type = user_content_type,
    )
    #member_list_permission = Permission.objects.get(codename = 'can_access_member_list')
    member_group.permissions.add(member_list_permission)
    officer_group.permissions.add(member_list_permission)
    owner_group.permissions.add(member_list_permission)

    full_member_list_permission = Permission.objects.create(
        codename = 'can_access_full_member_list_' + chess_club_name,
        name = 'Can access list of members with all information for club ' + chess_club_name,
        content_type = user_content_type,
    )
    #full_member_list_permission = Permission.objects.get(codename = 'can_access_full_member_list')
    officer_group.permissions.add(full_member_list_permission)
    owner_group.permissions.add(full_member_list_permission)

    applications_permission = Permission.objects.create(
        codename = 'can_accept_applications_' + chess_club_name,
        name = 'Can allow an applicant to become a member for club ' + chess_club_name,
        content_type = user_content_type,
    )
    #applications_permission = Permission.objects.get(codename = 'can_accept_applications')
    officer_group.permissions.add(applications_permission)

    remove_member_permission = Permission.objects.create(
        codename = 'can_remove_member_' + chess_club_name,
        name = 'Can remove a member from the club for club ' + chess_club_name,
        content_type = user_content_type,
    )
    #remove_member_permission = Permission.objects.get(codename = 'can_remove_member')
    officer_group.permissions.add(remove_member_permission)

    promote_permission = Permission.objects.create(
        codename = 'can_promote_member_' + chess_club_name,
        name = 'Can promote a member to an officer for club ' + chess_club_name,
        content_type = user_content_type,
    )
    #promote_permission = Permission.objects.get(codename = 'can_promote_member')
    owner_group.permissions.add(promote_permission)

    demote_permission = Permission.objects.create(
        codename = 'can_demote_officer_' + chess_club_name,
        name = 'Can demote an officer to a member for club ' + chess_club_name,
        content_type = user_content_type,
    )
    #demote_permission = Permission.objects.get(codename = 'can_demote_officer')
    owner_group.permissions.add(demote_permission)

    ownership_permission = Permission.objects.create(
        codename = 'can_transfer_ownership_' + chess_club_name,
        name = 'Can transfer owner status to an officer for club ' + chess_club_name,
        content_type = user_content_type,
    )
    #ownership_permission = Permission.objects.get(codename = 'can_transfer_ownership')
    owner_group.permissions.add(ownership_permission)

    become_owner_permission = Permission.objects.create(
        codename = 'can_become_owner_' + chess_club_name,
        name = 'Can receive ownership of club for club ' + chess_club_name,
        content_type = user_content_type,
    )
    #become_owner_permission = Permission.objects.get(codename = 'can_become_owner')
    officer_group.permissions.add(become_owner_permission)

#Creates first ChessClubGroups object to represent the first club - this may be moved elsewhere later.
club_list.append(new ChessClubGroups("First_Club"))
