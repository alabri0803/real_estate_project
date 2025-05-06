from django.db import models
from django.utils.translation import gettext_lazy as _
from contracts.models import Contract
from properties.models import Unit

class Invoice(models.Model):
  class InvoicType(models.TextChoices):
    RENT = 'rent', _('إيجار')
    SERVICE = 'service', _('خدمة')
    MAINTENANCE = 'maintenance', _('صيانة')
    PENALTY = 'penalty', _('غرامة')
    OTHER = 'other', _('أخرى')
  invoice_number = models.CharField(
    _('رقم الفاتورة'),
    max_length=50, 
    unique=True
  )
  contract = models.ForeignKey(
    Contract,
    on_delete=models.PROTECT,
    related_name='invoices',
    verbose_name=_('العقد'),
  )
  unit = models.ForeignKey(
    Unit,
    on_delete=models.PROTECT,
    related_name='invoices',
    verbose_name=_('الوحدة'),
  )
  invoice_type = models.CharField(
    _('نوع الفاتورة'),
    max_length=20,
    choices=InvoicType.choices,
    default=InvoicType.RENT,
  )
  issue_date = models.DateField(
    _('تاريخ الإصدار'),
    auto_now_add=True,
  )
  due_date = models.DateField(
    _('تاريخ الاستحقاق'),
  )
  amount = models.DecimalField(
    _('المبلغ'),
    max_digits=12,
    decimal_places=2,
  )
  vat_amount = models.DecimalField(
    _('ضريبة القيمة المضافة'),
    max_digits=12,
    decimal_places=2,
    default=0,
  )
  total_amount = models.DecimalField(
    _('المبلغ الإجمالي'),
    max_digits=12,
    decimal_places=2,
  )
  description = models.TextField(
    _('الوصف'),
    blank=True,
  )
  is_paid = models.BooleanField(
    _('تم السداد؟'),
    default=False,
  )
  created_at = models.DateTimeField(
    _('تاريخ الإنشاء'),
    auto_now_add=True,
  )

  class Meta:
    verbose_name = _('فاتورة')
    verbose_name_plural = _('الفواتير')
    ordering = ['-issue_date']

  def __str__(self):
    return f"{self.invoice_number} - {self.contract.tenant.name} - {self.total_amount} ر.ع."