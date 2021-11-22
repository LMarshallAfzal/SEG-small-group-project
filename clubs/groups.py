from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User

applicant_group, created = Group.objects.get_or_create(name = 'Applicant')
member_group, created = Group.objects.get_or_create(name = 'Member')
officer_group, created = Group.objects.get_or_create(name = 'Officer')
owner_group, created = Group.objects.get_or_create(name = 'Owner')

user_content_type = ContentType.objects.get_for_model(User)

member_list_permission = Permission.objects.create(
    codename = 'can_access_member_list',
    name = 'Can access a basic list of members and some details',
    content_type = user_content_type,
)
member_group.permissions.add(member_list_permission)
officer_group.permissions.add(member_list_permission)
owner_group.permissions.add(member_list_permission)

full_member_list_permission = Permission.objects.create(
    codename = 'can_access_full_member_list',
    name = 'Can access list of members with all information',
    content_type = user_content_type,
)
officer_group.permissions.add(full_member_list_permission)
owner_group.permissions.add(full_member_list_permission)

applications_permission = Permission.objects.create(
    codename = 'can_accept_applications',
    name = 'Can allow an applicant to become a member',
    content_type = user_content_type,
)
officer_group.permissions.add(applications_permission)

remove_member_permission = Permission.objects.create(
    codename = 'can_remove_member',
    name = 'Can remove a member from the club',
    content_type = user_content_type,
)
officer_group.permissions.add(remove_member_permission)

promote_permission = Permission.objects.create(
    codename = 'can_promote_member',
    name = 'Can promote a member to an officer',
    content_type = user_content_type,
)
officer_group.permissions.add(promote_permission)

demote_permission = Permission.objects.create(
    codename = 'can_demote_officer',
    name = 'Can demote an officer to a member',
    content_type = user_content_type,
)
owner_group.permissions.add(demote_permission)

ownership_permission = Permission.objects.create(
    codename = 'can_transfer_ownership',
    name = 'Can transfer owner status to an officer',
    content_type = user_content_type,
)
owner_group.permissions.add(ownership_permission)

become_owner_permission = Permission.objects.create(
    codename = 'can_become_owner',
    name = 'Can receive ownership of club',
    content_type = user_content_type,
)
officer_group.permissions.add(become_owner_permission)
