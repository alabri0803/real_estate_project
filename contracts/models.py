from django.db import models
from django.utils.translation import gettext_lazy as _

from agents.models import RealEstateAgent
from properties.models import Unit
from tenants.models import Company


class Contract(models.Model):
  class ContractType(models.TextChoices):
    COMMERCIAL_LEASE = 'commercial_lease', _('إيجار تجاري')
    RESIDENTIAL_LEASE = 'residential_lease', _('إيجار سكني')
    INVESTMENT = 'investment', _('استثمار')
    SALE = 'sale', _('بيع')
    COMPANY_SHARES = 'company_shares', _('بيع حصص شركات')
  contract_number = models.CharField(
    _('رقم العقد'),
    max_length=50,
    unique=True,
  )
  contract_type = models.CharField(
    _('نوع العقد'),
    max_length=20,
    choices=ContractType.choices,
    default=ContractType.COMMERCIAL_LEASE,
  )
  unit = models.ForeignKey(
    Unit,
    on_delete=models.PROTECT,
    related_name='contracts',
    verbose_name=_('الوحدة العقارية'),
  )
  tenant = models.ForeignKey(
    Company,
    on_delete=models.PROTECT,
    related_name='contracts',
    verbose_name=_('المستأجر'),
  )
  agent = models.ForeignKey(
    RealEstateAgent,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    verbose_name=_('الوسيط العقاري'),
  )
  start_date = models.DateField(
    _('تاريخ البدء'),
  )
  end_date = models.DateField(
    _('تاريخ الانتهاء'),
  )
  monthly_rent = models.DecimalField(
    _('الإيجار الشهري'),
    max_digits=10,
    decimal_places=2,
    null=True,
    blank=True,
  )
  total_amount = models.DecimalField(
    _('المبلغ الإجمالي'),
    max_digits=10,
    decimal_places=2,
    null=True,
    blank=True,
  )
  secrity_deposit = models.DecimalField(
    _('الضمان المالي'),
    max_digits=10,
    decimal_places=2,
    null=True,
    blank=True,
  )
  paymnet_terms = models.TextField(
    _('شروط السداد'),
    blank=True,
  )
  special_terms = models.TextField(
    _('شروط خاصة'),
    blank=True,
  )
  is_active = models.BooleanField(
    _('نشط'),
    default=True,
  )
  created_at = models.DateTimeField(
    _('تاريخ الإنشاء'),
    auto_now_add=True,
  )
  updated_at = models.DateTimeField(
    _('تاريخ التحديث'),
    auto_now=True,
  )

  class Meta:
    verbose_name = _('عقد')
    verbose_name_plural = _('العقود')
    ordering = ['-start_date']

  def __str__(self):
    return f"{self.contract_number} - {self.unit} - {self.tenant.name}"

class ContractDocument(models.Model):
  contract = models.ForeignKey(
    Contract,
    on_delete=models.CASCADE,
    related_name='documents',
    verbose_name=_('العقد'),
  )
  document_type = models.CharField(
    _('نوع المستند'),
    max_length=50,
    choices=[
      ('contract_copy', _('نسخه من العقد')),
      ('id_copy', _('نسخه من الهوية/السجل التجاري')),
      ('insurance', _('وثيقة التأمين')),
      ('other', _('مستند أخرى'))
    ]
  )
  file = models.FileField(
    _('الملف'),
    upload_to='contracts/documents/',
  )
  uploaded_date = models.DateTimeField(
    _('تاريخ الرفع'),
    auto_now_add=True
  )
  notes = models.TextField(
    _('ملاحظات'),
    blank=True,
  )

  class Meta:
    verbose_name = _('مستند العقد')
    verbose_name_plural = _('مستندات العقود')

  def __str__(self):
    return f"{self.contract.contract_number} - {self.get_document_type_display()}"