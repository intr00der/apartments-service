# Generated by Django 3.2.2 on 2021-06-01 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_born_in_user_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_owner',
        ),
    ]
