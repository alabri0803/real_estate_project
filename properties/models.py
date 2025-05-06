from django.db import models
from django.utils.translation import gettext_lazy as _


class Building(models.Model):
  class BuildingType(models.TextChoices):
    COMMERCIAL = 'commercial', _('تجاري')
    RESIDENTIAL = 'residential', _('سكني')
    MIXED = 'mixed', _('مختلط')
  name = models.CharField(
    _('اسم المبنى'), 
    max_length=100
  )
  building_type = models.CharField(
    _('نوع المبنى'),
    max_length=20,
    choices=BuildingType.choices,
    default=BuildingType.COMMERCIAL
  )
  address = models.TextField(
    _('العنوان'),
  )
  city = models.CharField(
    _('المدينة'),
    max_length=50
  )
  total_floors = models.PositiveIntegerField(
    _('إجمالي الطوابق'),
  )
  created_at = models.DateTimeField(
    _('تاريخ الإنشاء'),
    auto_now_add=True
  )

  class Meta:
    verbose_name = _('مبنى')
    verbose_name_plural = _('المباني')

  def __str__(self):
    return self.name

class Floor(models.Model):
  building = models.ForeignKey(
    Building,
    on_delete=models.CASCADE,
    related_name='floors',
    verbose_name=_('المبنى')
  )
  floor_number = models.PositiveIntegerField(
    _('رقم الطابق'),
  )
  total_units = models.PositiveIntegerField(
    _('إجمالي الوحدات'),
  )

  class Meta:
    verbose_name = _('طابق')
    verbose_name_plural = _('الطوابق')
    unique_together = ('building', 'floor_number')

  def __str__(self):
    return f"{self.building.name} - {_('طابق')} {self.floor_number}"

class Unit(models.Model):
  class UnitType(models.TextChoices):
    APARTMENT = 'apartment', _('شقة')
    OFFICE = 'office', _('مكتب')
    STORE = 'store', _('محل تجاري')
    WAREHOUSE = 'warehouse', _('مستودع')
  floor = models.ForeignKey(
    Floor,
    on_delete=models.CASCADE,
    related_name='units',
    verbose_name=_('الطابق')
  )
  unit_number = models.CharField(
    _('رقم الوحدة'),
    max_length=20
  )
  unit_type = models.CharField(
    _('نوع الوحدة'),
    max_length=20,
    choices=UnitType.choices,
    default=UnitType.OFFICE
  )
  area = models.DecimalField(
    _('المساحة(متر مربع)'),
    max_digits=10,
    decimal_places=2
  )
  status = models.CharField(
    _('الحالة'),
    max_length=20,
    choices=[
      ('vacant', _('شاغر')),
      ('occupied', _('مشغول')),
      ('under_construction', _('تحت الصيانة')),
    ],
    default='vacant'
  )

  class Meta:
    verbose_name = _('وحدة')
    verbose_name_plural = _('الوحدات')
    unique_together = ('floor', 'unit_number')

  def __str__(self):
    return f"{self.floor.building.name} - {self.unit_number}"