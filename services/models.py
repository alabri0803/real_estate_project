from django.db import models
from django.utils.translation import gettext_lazy as _

from properties.models import Building


class ServiceType(models.Model):
  name = models.CharField(
    _('اسم الخدمة'),
    max_length=100,
  )
  description = models.TextField(
    _('وصف الخدمة'),
    blank=True,
  )
  is_active = models.BooleanField(
    _('نشط؟'),
    default=True,
  )

  class Meta:
    verbose_name = _('نوع الخدمة')
    verbose_name_plural = _('أنواع الخدمات')

  def __str__(self):
    return self.name

class ServiceContract(models.Model):
  service_type = models.ForeignKey(
    ServiceType,
    on_delete=models.PROTECT,
    related_name='contracts',
    verbose_name=_('نوع الخدمة'),
  )
  building = models.ForeignKey(
    Building,
    on_delete=models.PROTECT,
    related_name='service_contracts',
    verbose_name=_('المبنى'),
  )
  provider_name = models.CharField(
    _('اسم مقدم الخدمة'),
    max_length=200,
  )
  contract_number = models.CharField(
    _('رقم العقد'),
    max_length=50,
  )
  start_date = models.DateField(
    _('تاريخ البدء'),
  )
  end_date = models.DateField(
    _('تاريخ الانتهاء'),
  )
  monthly_cost = models.DecimalField(
    _('التكلفة الشهرية'),
    max_digits=12,
    decimal_places=2,
  )
  terms = models.TextField(
    _('شروط العقد'),
    blank=True,
  )
  is_active = models.BooleanField(
    _('نشط؟'),
    default=True,
  )

  class Meta:
    verbose_name = _('عقد خدمة')
    verbose_name_plural = _('عقود الخدمات')

  def __str__(self):
    return f"{self.service_type.name} - {self.building.name}"

class ServiceInvoice(models.Model):
  service_contract = models.ForeignKey(
    ServiceContract,
    on_delete=models.PROTECT,
    related_name='invoices',
    verbose_name=_('عقد الخدمة'),
  )
  invoice_number = models.CharField(
    _('رقم الفاتورة'),
    max_length=50,
    unique=True,
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
  description = models.TextField(
    _('الوصف'),
    blank=True,
  )
  is_paid = models.BooleanField(
    _('تم السداد؟'),
    default=False,
  )

  class Meta:
    verbose_name = _('فاتورة خدمة')
    verbose_name_plural = _('فواتير الخدمات')

  def __str__(self):
    return f"{self.invoice_number} - {self.service_contract.provider_name}"