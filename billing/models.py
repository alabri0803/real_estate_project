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

class Payment(models.Model):
  class PaymentMethod(models.TextChoices):
    CASH = 'cash', _('نقدي')
    BANK_TRANSFER = 'bank_transfer', _('حوالة بنكية')
    CHEQUE = 'cheque', _('شيك')
    CREDIT_CARD = 'credit_card', _('بطاقة ائتمان')
    OTHER = 'other', _('أخرى')
  invoice = models.ForeignKey(
    Invoice,
    on_delete=models.PROTECT,
    related_name='payments',
    verbose_name=_('الفاتورة'),
  )
  payment_number = models.CharField(
    _('رقم السداد'),
    max_length=50,
    unique=True,
  )
  payment_date = models.DateField(
    _('تاريخ السداد'),
  )
  amount = models.DecimalField(
    _('المبلغ'),
    max_digits=12,
    decimal_places=2,
  )
  payment_method = models.CharField(
    _('طريقة السداد'),
    max_length=20,
    choices=PaymentMethod.choices,
    default=PaymentMethod.BANK_TRANSFER,
  )
  reference_number = models.CharField(
    _('رقم المرجع'),
    max_length=100,
    blank=True,
  )
  notes = models.TextField(
    _('ملاحظات'),
    blank=True,
  )
  receipt_attachment = models.FileField(
    _('إيصال السداد'),
    upload_to='payments/receipts/',
    blank=True,
    null=True,
  )
  created_at = models.DateTimeField(
    _('تاريخ الإنشاء'),
    auto_now_add=True,
  )

  class Meta:
    verbose_name = _('سداد')
    verbose_name_plural = _('السدادات')
    ordering = ['-payment_date']

  def __str__(self):
    return f"{self.payment_number} - {self.invoice.invoice_number} - {self.amount} ر.ع."