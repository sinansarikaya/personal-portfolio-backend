# Generated by Django 4.2.1 on 2023-06-10 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_first_name_profile_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
    ]
