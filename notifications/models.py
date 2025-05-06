from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class Notification(models.Model):
  NOTIFICATION_TYPES = [
    ('contract_expiry', _('انتهاء العقد')),
    ('payment_due', _('استحقاق دفعة')),
    ('document_expiry', _('انتهاء صلاحية مستند')),
    ('custom', _('إشعار مخصص'))
  ]
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='notifications',
    verbose_name=_('المستخدم'),
  )
  notification_type = models.CharField(
    _('نوع الإشعار'),
    max_length=50,
    choices=NOTIFICATION_TYPES,
  )
  title = models.CharField(
    _('العنوان'),
    max_length=200
  )
  message = models.TextField(
    _('الرسالة'),
  )
  is_read = models.BooleanField(
    _('تم القراءة؟'),
    default=False
  )
  related_url = models.URLField(
    _('رابط ذات صلة'),
    blank=True,
    null=True,
  )
  created_at = models.DateTimeField(
    _('وقت الإنشاء'),
    auto_now_add=True
  )

  class Meta:
    verbose_name = _('إشعار')
    verbose_name_plural = _('الإشعارات')
    ordering = ['-created_at']

  def __str__(self):
    return f"{self.user.username} - {self.title}"

  def mark_as_read(self):
    self.is_read = True
    self.save()