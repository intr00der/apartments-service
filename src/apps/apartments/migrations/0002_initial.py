# Generated by Django 3.2.2 on 2021-05-17 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apartments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='apartment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', to='apartments.apartment'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='region',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='apartments.country'),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='apartments.region'),
        ),
        migrations.AddField(
            model_name='apartmentphoto',
            name='apartment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='apartments.apartment'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='apartments', to='apartments.city'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='apartments', to='apartments.country'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='apartment',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='apartments', to='apartments.region'),
        ),
    ]
