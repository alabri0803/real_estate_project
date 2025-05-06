from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
  USER_TYPE = [
    ('admin', _('مدير النظام')),
    ('property_manager', _('مدير عقارات')),
    ('accountant', _('محاسب')),
    ('agent', _('وسيط عقاري')),
    ('client', _('عميل')),
  ]
  user_type = models.CharField(
    _('نوع المستخدم'),
    max_length=20,
    choices=USER_TYPE,
    default='property_manager'
  )
  phone = models.CharField(
    _('رقم الهاتف '),
    max_length=20,
    blank=True,
  )
  address = models.TextField(
    _('العنوان'),
    blank=True,
  )
  city = models.CharField(
    _('المدينة'),
    max_length=100,
    blank=True,
  )
  profile_picture = models.ImageField(
    _('صورة الملف الشخصي'),
    upload_to='accounts/profile_pictures/',
    blank=True,
    null=True,
  )
  is_verified = models.BooleanField(
    _('موثق؟'),
    default=False,
  )
  omani_id = models.CharField(
    _('رقم البطاقة الشخصية'),
    max_length=20,
    blank=True,
    unique=True,
    null=True,
  )

  class Meta:
    verbose_name = _('مستخدم')
    verbose_name_plural = _('المستخدمون')

  def __str__(self):
    return f"{self.get_full_name()} - {self.username}"

class UserActivityLog(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='activity_logs',
    verbose_name=_('المستخدم'),
  )
  action = models.CharField(
    _('الإجراء'),
    max_length=100,
  )
  details = models.TextField(
    _('التفاصيل'),
    blank=True,
  )
  ip_address = models.GenericIPAddressField(
    _('عنوان IP'),
    blank=True,
    null=True,
  )
  created_at = models.DateTimeField(
    _('وقت الإنشاء'),
    auto_now_add=True
  )

  class Meta:
    verbose_name = _('سجل نشاط المستخدم')
    verbose_name_plural = _('سجلات نشاط المستخدمين')
    ordering = ['-created_at']

  def __str__(self):
    return f"{self.user.username} - {self.action}"

class CustomPermission:
  class Meta:
    permissions = [
      ('manage_properties', _('إدارة العقارات')),
      ('manage_contracts', _('إدارة العقود')),
      ('manage_invoices', _('إدارة الفواتير')),
      ('manage_reports', _('إنشاء التقارير')),
      ('view_dashboard', _('عرض لوحة التحكم')),
      ('manage_users', _('إدارة المستخدمين'))
    ]