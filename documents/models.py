from django.db import models
from django.utils.translation import gettext_lazy as _

from contracts.models import Contract
from tenants.models import Company


class DocumentTemplate(models.Model):
  DOCUMENT_TYPES = [
    ('official_letter', _('رسالة رسمية')),
    ('legal_notice', _('إنذار قانوني')),
    ('contract', _('عقد')),
    ('certificate', _('شهادة')),
    ('eviction_notice', _('إشعار إخلاء')),
    ('rent_increase', _('إشعار زيادة إيجار'))
  ]
  name = models.CharField(
    _('اسم القالب'),
    max_length=100,
  )
  document_type = models.CharField(
    _('نوع المستند'),
    max_length=50,
    choices=DOCUMENT_TYPES,
  )
  template_file = models.FileField(
    _('ملف القالب'),
    upload_to='documents/templates/',
  )
  variables = models.TextField(
    _('المتغيرات المتاحة'),
    help_text=_('قائمة بالمتغيرات التي يمكن استخدامها في القالب، مفصولة بفاصلة')
  )
  is_active = models.BooleanField(
    _('نشط؟'),
    default=True
  )

  class Meta:
    verbose_name = _('قالب مستند')
    verbose_name_plural = _('قوالب المستندات')

  def __str__(self):
    return f"{self.get_document_type_display()} - {self.name}"

class GeneratedDocument(models.Model):
  contract = models.ForeignKey(
    Contract,
    on_delete=models.PROTECT,
    related_name='generated_documents',
    verbose_name=_('العقد'),
    null=True,
    blank=True,
  )
  company = models.ForeignKey(
    Company,
    on_delete=models.PROTECT,
    related_name='documents',
    verbose_name=_('الشركة'),
    null=True,
    blank=True
  )
  template = models.ForeignKey(
    DocumentTemplate,
    on_delete=models.PROTECT,
    verbose_name=_('القالب المستخدم'),
  )
  document_number = models.CharField(
    _('رقم المستند'),
    max_length=50,
    unique=True,
  )
  issue_date = models.DateField(
    _('تاريخ الإصدار'),
    auto_now_add=True
  )
  document_file = models.FileField(
    _('ملف المستند'),
    upload_to='documents/generated/',
  )
  notes = models.TextField(
    _('ملاحظات'),
    blank=True,
  )

  class Meta:
    verbose_name = _('مستند تم إنشاؤه')
    verbose_name_plural = _('المستندات التي تم إنشاؤها')
    ordering = ['-issue_date']

  def __str__(self):
    return f"{self.document_number} - {self.template.get_document_type_display()}"