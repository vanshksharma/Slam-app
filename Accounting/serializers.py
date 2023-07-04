from rest_framework import serializers
from .models import Proposal, Invoice, Payment, Item


class ProposalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Proposal
        fields='__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Invoice
        fields='__all__'


class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Payment
        fields='__all__'

class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Item
        fields='__all__'
        