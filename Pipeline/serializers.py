from rest_framework import serializers
from .models import Contact, Lead, Address


class ContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Contact
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