from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
  if created:
    group_name = None
    if instance.user_type == 'admin':
      group_name = 'Admins'
    elif instance.user_type == 'property_manager':
      group_name = 'Property Managers'
    elif instance.user_type == 'accountant':
      group_name = 'Accountants'
    elif instance.user_type == 'agent':
      group_name = 'Agents'
    if group_name:
      group, _ = Group.objects.get_or_create(name=group_name)
      instance.groups.add(group)