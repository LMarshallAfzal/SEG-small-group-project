# Generated by Django 3.2.5 on 2021-12-12 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0019_club_club_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='club_owner',
            field=models.ForeignKey(default='billie@example.org', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
