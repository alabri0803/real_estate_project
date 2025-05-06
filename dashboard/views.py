from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from contracts.models import Contract
from billing.models import Invoice
from properties.models import Unit
from django.utils.timezone import now
from django.db.models import Count, Sum, Q
from django.utils.translation import gettext_lazy as _

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # إحصائيات العقود
        contracts = Contract.objects.filter(
            Q(created_by=user) | Q(agent__user=user)

        active_contracts = contracts.filter(
            is_active=True,
            end_date__gte=now().date()
        ).count()

        expiring_soon = contracts.filter(
            is_active=True,
            end_date__range=[now().date(), now().date() + timedelta(days=30)]
        ).count()

        # إحصائيات الفواتير
        invoices = Invoice.objects.filter(
            contract__in=contracts.values_list('id', flat=True)
        )

        paid_invoices = invoices.filter(is_paid=True).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        unpaid_invoices = invoices.filter(
            is_paid=False,
            due_date__lt=now().date()
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # الوحدات الشاغرة
        vacant_units = Unit.objects.filter(
            status='vacant'
        ).count()

        context.update({
            'active_contracts': active_contracts,
            'expiring_soon': expiring_soon,
            'paid_invoices': paid_invoices,
            'unpaid_invoices': unpaid_invoices,
            'vacant_units': vacant_units,
        })

        return context