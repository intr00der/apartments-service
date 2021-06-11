# Generated by Django 3.2.2 on 2021-06-03 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingmessage',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_booking_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookingmessage',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_booking_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
