# Generated by Django 3.2.5 on 2021-12-10 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0013_auto_20211210_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='club_location',
            field=models.CharField(max_length=100),
        ),
    ]
