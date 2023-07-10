from rest_framework import serializers
from .models import UserProfile, Integrations
from timezone_field.rest_framework import TimeZoneSerializerField


class ProfileSerializer(serializers.ModelSerializer):
    timezone=TimeZoneSerializerField()
    
    class Meta:
        model=UserProfile
        fields='__all__'


class IntegrationsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Integrations
        fields='__all__'