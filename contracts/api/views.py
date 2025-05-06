from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsPropertyManagerOrAdmin

from ..models import Contract, ContractDocument
from .serializers import ContractDocumentSerializer, ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):
  queryset = Contract.objects.all().select_related('unit', 'tenant', 'agent').prefetch_related('documents')
  serializer_class = ContractSerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  filterset_fields = ['contract_type', 'is_active', 'unit__unit_number']
  search_fields = ['contract_number', 'tenant__name', 'unit__unit_number']
  ordering_fields = ['start_date', 'end_date', 'monthly_rent']
  permission_classes = [IsAuthenticated, IsPropertyManagerOrAdmin]

  def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)

class ContractDocumentViewSet(viewsets.ModelViewSet):
  queryset = ContractDocument.objects.all()
  serializer_class = ContractDocumentSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return super().get_queryset().filter(
      contract_id = self.kwargs['contract_pk']
    )

  def perform_create(self, serializer):
    serializer.save(
      contract_id = self.kwargs['contract_pk'],
      uploaded_by = self.request.user
    )