from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=(
        ('client','Клиент'), ('manager','Менеджер'), ('admin','Админ')
    ), default='client')
    # другие поля профиля

    def __str__(self):
        return f"Profile({self.user.username})"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # опционально: сохранять профиль при каждом сохранении User
        try:
            instance.profile.save()
        except Exception:
            # если профиль всё равно отсутствует — создать
            Profile.objects.get_or_create(user=instance)
