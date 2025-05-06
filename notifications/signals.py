from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from contracts.models import Contract

from .models import Notification


@receiver(post_save, sender=Contract)
def create_contract_expiry_notification(sender, instance, created, **kwargs):
  if not created and instance.end_date:
    days_left = (instance.end_date - now().date()).days
    if days_left <= 30:
      Notification.objects.create(
        user=instance.created_by,
        notification_type='contract_expiry',
        title=_('تنبيه انتهاء العقد'),
        message=_('العقد {contract_number} سينتهي خلال 30 يوم').format(contract_number=instance.contract_number),
        related_url=instance.get_absolute_url(),
      )