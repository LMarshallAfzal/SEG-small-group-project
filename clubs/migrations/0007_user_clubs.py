# Generated by Django 3.2.5 on 2021-12-06 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0006_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='clubs',
            field=models.CharField(choices=[('Kerbal Chess Club', 'Kerbal Chess Club'), ('KCL Chess Society', 'KCL Chess Society'), ('UCL Terrible Chess Team', 'UCL Terrible Chess Team'), ('Elite Cambridge Chess Team', 'Elite Cambridge Chess Team')], default='Kerbal Chess Club', max_length=50),
        ),
    ]
