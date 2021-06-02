# Generated by Django 3.2.2 on 2021-06-01 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apartments', '0003_alter_review_rating'),
        ('chat', '0004_auto_20210601_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingmessage',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_messages', to='apartments.booking'),
        ),
        migrations.AlterField(
            model_name='bookingmessage',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_booking_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookingmessage',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_booking_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
