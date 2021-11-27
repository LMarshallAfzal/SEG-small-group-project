# Generated by Django 3.2.5 on 2021-11-20 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('can_access_member_list', 'Can access a basic list of members and some details'), ('can_access_full_member_list', 'Can access list of members with all information'), ('can_accept_applications', 'Can allow an applicant to become a member'), ('can_remove_member', 'Can remove a member from the club'), ('can_promote_member', 'Can promote a member to an officer'), ('can_demote_officer', 'Can demote an officer to a member'), ('can_transfer_ownership', 'Can transfer owner status to an officer'), ('can_become_owner', 'Can receive ownership of club')]},
        ),
    ]
