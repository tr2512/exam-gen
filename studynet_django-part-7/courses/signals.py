from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def assign_group_to_new_user(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='User') 
        instance.groups.add(group)