from rest_framework import serializers
from .models import LoginUser


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=LoginUser
        fields='__all__'
        extra_kwargs={
            'password': {'write_only': True}
        }


class InputSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)