from rest_framework import serializers
from .models import Customer, Lead, Address


class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Customer
        fields='__all__'


class LeadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Lead
        fields='__all__'
        read_only_fields = ['amount_paid']


class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Address
        fields='__all__'  