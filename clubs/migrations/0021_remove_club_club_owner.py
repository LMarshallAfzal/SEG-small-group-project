# Generated by Django 3.2.5 on 2021-12-13 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0020_alter_club_club_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='club_owner',
        ),
    ]
