# Generated by Django 3.2.2 on 2021-05-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Female'), (2, 'Male'), (3, 'Other')]),
        ),
    ]
