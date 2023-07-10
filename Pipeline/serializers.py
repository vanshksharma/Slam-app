from rest_framework import serializers
from .models import Contact, Lead


class ContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Contact
        fields='__all__'


class LeadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Lead
        fields='__all__'
