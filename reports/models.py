from django.db import models
from django.utils.translation import gettext_lazy as _
from contracts.models import Contract
from properties.models import Building

class ReportTemplate(models.Model):
  REPORT_TYPES = [
    ('financial', _('مالي')),
    ('occupancy', _('نسبة الإشغال')),
    ('rent_collection', _('تحصيل الإيجار')),
    ('expenses', _('المصروفات')),
    ('custom', _('تقرير مخصص'))
  ]
  name = models.CharField(
    _('اسم التقرير'),
    max_length=100,
  )
  report_type = models.CharField(
    _('نوع التقرير'),
    max_length=50,
    choices=REPORT_TYPES,
  )
  template_file = models.FileField(
    _('ملف القالب'),
    upload_to='reports/templates/',
    null=True,
    blank=True
  )
  sql_query = models.TextField(
    _('استعلام SQL'),
    blank=True,
    help_text=_('استخدم {building.id} و {start_date} و {end_date} كمتغيرات'),
  )
  is_active = models.BooleanField(
    _('نشط؟'),
    default=True
  )

  class Meta:
    verbose_name = _('قالب تقرير')
    verbose_name_plural = _('قوالب التقارير')

  def __str__(self):
    return f"{self.get_report_type_display()} - {self.name}"

class GeneratedReport(models.Model):
  building = models.ForeignKey(
    Building,
    on_delete=models.PROTECT,
    related_name='reports',
    verbose_name=_('المبنى'),
    null=True,
    blank=True,
  )
  template = models.ForeignKey(
    ReportTemplate,
    on_delete=models.PROTECT,
    verbose_name=_('قالب التقرير'),
  )
  report_number = models.CharField(
    _('رقم التقرير'),
    max_length=50,
    unique=True,
  )
  start_date = models.DateField(
    _('تاريخ البداية'),
  )
  end_date = models.DateField(
    _('تاريخ النهاية')
  )
  generated_at = models.DateTimeField(
    _('تاريخ الإنشاء'),
    auto_now_add=True
  )
  report_file = models.FileField(
    _('ملف التقرير'),
    upload_to='reports/generated/',
  )
  perameters = models.TextField(
    _('معلمات التقرير'),
    default=dict,
    blank=True,
  )

  class Meta:
    verbose_name = _('تقرير تم إنشاؤه')
    verbose_name_plural = _('التقارير التي تم إنشاؤها')
    ordering = ['-generated_at']

  def __str__(self):
    return f"{self.report_number} - {self.template.name}"

class Notification(models.Model):
  NOTIFICATION_TYPES = [
    ('contract_expiry', _('انتهاء العقد')),
    ('payment_due', _('استحقاق دفعة')),
    ('document_expiry', _('انتهاء صلاحية مستند')),
    ('custom', _('إشعار مخصص'))
  ]
  contract = models.ForeignKey(
    Contract,
    on_delete=models.CASCADE,
    related_name='notifications',
    verbose_name=_('العقد'),
    null=True,
    blank=True,
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
  due_date = models.DateField(
    _('تاريخ الاستحقاق'),
  )
  is_sent = models.BooleanField(
    _('تم الإرسال؟'),
    default=False
  )
  sent_at = models.DateTimeField(
    _('وقت الإرسال'),
    auto_now_add=True,
    null=True,
    blank=True
  )
  created_at = models.DateTimeField(
    _('وقت الإنشاء'),
    auto_now_add=True
  )

  class Meta:
    verbose_name = _('إشعار')
    verbose_name_plural = _('الإشعارات')
    ordering = ['-due_date']

  def __str__(self):
    return f"{self.get_notification_type_display()} - {self.title}"