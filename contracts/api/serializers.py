from django.utils.timezone import now
from rest_framework import serializers

from properties.api.serializers import UnitSimpleSerializer
from tenants.api.serializers import CompanySimpleSerializer

from ..models import Contract, ContractDocument


class ContractSerializer(serializers.ModelSerializer):
  unit_details = UnitSimpleSerializer(source='unit', read_only=True)
  tenant_details = CompanySimpleSerializer(source='tenant', read_only=True)
  remaining_days = serializers.SerializerMethodField()
  class Meta:
    model = Contract
    read_only_fields = ['created_at', 'updated_at']
    extra_kwargs = {
      'security_deposit': {'required': False},
      'agent': {'required': False},
    }
  def get_remaining_days(self, obj):
    if obj.end_date:
      return (obj.end_date - now().date()).days
    return None

class ContractDocumentSerializer(serializers.ModelSerializer):
  document_url = serializers.SerializerMethodField()
  class Meta:
    model = ContractDocument
    fields = '__all__'
    read_only_fields = ['upload_date']
  def get_document_url(self, obj):
    request = self.context.get('request')
    if obj.file and request:
      return request.build_absolute_uri(obj.file.url)
    return None