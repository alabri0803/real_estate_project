from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class RealEstateAgent(models.Model):
  user = models.OneToOneField(
    User, 
    on_delete=models.CASCADE,
    related_name='real_estate_agent',
    verbose_name=_('حساب المستخدم')
  )
  license_number = models.CharField(
    _('رقم الرخصة'),
    max_length=50,
    unique=True,
  )
  agency_name = models.CharField(
    _('اسم الوكالة'),
    max_length=100,
  )
  phone = models.CharField(
    _('الهاتف'),
    max_length=20,
  )
  email = models.EmailField(
    _('البريد الإلكتروني'),
  )
  address = models.TextField(
    _('العنوان'),
  )
  specialization = models.CharField(
    _('التخصص'),
    max_length=50,
    choices=[
      ('commercial', _('عقارات تجارية')),
      ('residential', _('عقارات سكنية')),
      ('industrial', _('عقارات صناعية')),
      ('all', _('كل أنواع العقارات')),
    ],
    default='all',
  )
  is_active = models.BooleanField(
    _('نشط'),
    default=True,
  )

  class Meta:
    verbose_name = _('وسيط عقاري')
    verbose_name_plural = _('الوسطاء العقاريون')

  def __str__(self):
    return f"{self.user.get_full_name()} - {self.agency_name}"