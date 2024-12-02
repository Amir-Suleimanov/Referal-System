from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile
from .utils import generate_invite_code

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        invite_code = generate_invite_code()
        Profile.objects.create(user=instance, invite_code=invite_code)
