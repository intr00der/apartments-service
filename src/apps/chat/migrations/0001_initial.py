# Generated by Django 3.2.2 on 2021-06-03 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_messages', to='apartments.booking')),
            ],
        ),
    ]
