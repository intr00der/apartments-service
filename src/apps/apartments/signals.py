from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Apartment, Review


@receiver(post_save, sender=Review)
def calculate_average_rating(sender, instance, **kwargs):
    avg = Review.objects.filter(apartment_id=instance.apartment.pk).aggregate(Avg('rating'))
    instance.apartment.average_rating = round(avg['rating__avg'], 2)
    instance.apartment.save()
