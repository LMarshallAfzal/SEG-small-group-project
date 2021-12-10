# Generated by Django 3.2.5 on 2021-12-09 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0009_club_mission_statement'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='club_location',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='member_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]