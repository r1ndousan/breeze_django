# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance, defaults={'role': Profile.ROLE_CLIENT})
    else:
        # на случай, если профиль удалили вручную — восстановим
        Profile.objects.get_or_create(user=instance)
