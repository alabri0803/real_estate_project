from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
  class CompanyType(models.TextChoices):
    LLC = 'llc', _('شركة مساهمة محدودة')
    SAOC = 'saoc', _('شركة مساهمة عمانية عامة')
    SAOG = 'saog', _('شركة مساهمة عمانية مغلقة')
    INDIVIDUAL = 'individual', _('فردي')
  name = models.CharField(
    _('اسم الشركة/المستأجر'),
    max_length=200
  )
  commercial_registration = models.CharField(
    _('السجل التجاري'),
    max_length=50,
    unique=True
  )
  company_type = models.CharField(
    _('نوع الكيان'),
    max_length=20,
    choices=CompanyType.choices,
    default=CompanyType.LLC
  )
  tax_card = models.CharField(
    _('البطاقة الضريبية'),
    max_length=50,
    blank=True,
  )
  contact_person = models.CharField(
    _('الشخص المسئول'),
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
  city = models.CharField(
    _('المدينة'),
    max_length=50
  )
  country = models.CharField(
    _('الدولة'),
    max_length=50,
    default='عُمان'
  )
  is_active = models.BooleanField(
    _('نشط'),
    default=True
  )

  class Meta:
    verbose_name = _('شركة مستأجرة')
    verbose_name_plural = _('الشركات المستأجرة')

  def __str__(self):
    return self.name

class CompanyRepresentative(models.Model):
  company = models.ForeignKey(
    Company,
    on_delete=models.CASCADE,
    related_name='representatives',
    verbose_name=_('الشركة')
  )
  name = models.CharField(
    _('اسم الممثل'),
    max_length=100
  )
  position = models.CharField(
    _('المنصب'),
    max_length=100
  )
  phone = models.CharField(
    _('الهاتف'),
    max_length=20,
  )
  email = models.EmailField(
    _('البريد الإلكتروني'),
  )
  is_primary = models.BooleanField(
    _('الممثل الرئيسي'),
    default=False
  )

  class Meta:
    verbose_name = _('ممثل الشركة')
    verbose_name_plural = _('ممثلي الشركات')

  def __str__(self):
    return f"{self.name} - {self.company.name}"