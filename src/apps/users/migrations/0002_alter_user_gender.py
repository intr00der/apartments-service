# Generated by Django 3.2.2 on 2021-05-17 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[(1, 'Female'), (2, 'Male'), (3, 'Other')], max_length=6),
        ),
    ]