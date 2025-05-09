# Generated by Django 5.0.2 on 2025-05-06 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='اسم الشركة/المستأجر')),
                ('commercial_registration', models.CharField(max_length=50, unique=True, verbose_name='السجل التجاري')),
                ('company_type', models.CharField(choices=[('llc', 'شركة مساهمة محدودة'), ('saoc', 'شركة مساهمة عمانية عامة'), ('saog', 'شركة مساهمة عمانية مغلقة'), ('individual', 'فردي')], default='llc', max_length=20, verbose_name='نوع الكيان')),
                ('tax_card', models.CharField(blank=True, max_length=50, verbose_name='البطاقة الضريبية')),
                ('contact_person', models.CharField(max_length=100, verbose_name='الشخص المسئول')),
                ('phone', models.CharField(max_length=20, verbose_name='الهاتف')),
                ('email', models.EmailField(max_length=254, verbose_name='البريد الإلكتروني')),
                ('address', models.TextField(verbose_name='العنوان')),
                ('city', models.CharField(max_length=50, verbose_name='المدينة')),
                ('country', models.CharField(default='عُمان', max_length=50, verbose_name='الدولة')),
                ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
            ],
            options={
                'verbose_name': 'شركة مستأجرة',
                'verbose_name_plural': 'الشركات المستأجرة',
            },
        ),
        migrations.CreateModel(
            name='CompanyRepresentative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='اسم الممثل')),
                ('position', models.CharField(max_length=100, verbose_name='المنصب')),
                ('phone', models.CharField(max_length=20, verbose_name='الهاتف')),
                ('email', models.EmailField(max_length=254, verbose_name='البريد الإلكتروني')),
                ('is_primary', models.BooleanField(default=False, verbose_name='الممثل الرئيسي')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='representatives', to='tenants.company', verbose_name='الشركة')),
            ],
            options={
                'verbose_name': 'ممثل الشركة',
                'verbose_name_plural': 'ممثلي الشركات',
            },
        ),
    ]
