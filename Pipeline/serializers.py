from rest_framework import serializers
from .models import Customer, Lead, Address
from Auth.serializers import UserSerializer


class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Customer
        fields='__all__'


class LeadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Lead
        fields='__all__'


class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Address
        fields='__all__'  