from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    SEAT_PREFERENCES = (
        ('none','No Preference'),
        ('window','Window Seat'),
        ('isle','Isle Seat'),
    )
    MEAL_PREFERENCES = (
        ('none','No Preference'),
        ('veg','Vegitarian'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    zip_code = models.CharField(max_length=30, blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    credit_card = models.CharField(max_length=30, blank=True)
    seat_preference = models.CharField(max_length=30, default='none', blank=False, choices=SEAT_PREFERENCES)
    meal_preference = models.CharField(max_length=30, default='none', blank=False, choices=MEAL_PREFERENCES)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
