# Generated by Django 3.2.5 on 2021-12-13 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0021_remove_club_club_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='experience_level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=12),
        ),
    ]
