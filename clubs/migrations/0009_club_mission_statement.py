# Generated by Django 3.2.5 on 2021-12-09 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0008_remove_user_clubs'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='mission_statement',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
