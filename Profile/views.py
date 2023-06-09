from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Auth.decorators import auth_user
from .models import UserProfile, Integrations
from .serializers import ProfileSerializer,IntegrationsSerializer
from Auth.models import LoginUser
from Auth.serializers import UserSerializer
import bcrypt
from rest_framework import serializers
from Auth.utils import google_get_tokens
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.conf import settings
from .utils import get_zoom_tokens
# No Post and Delete API'S because profile gets automatically created at the time of signup and user cannot delete a profile, he/she can only delete the account.


class ProfileHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        profile=UserProfile.objects.get(user=user_dict['id'])
        profile_json=ProfileSerializer(profile).data
        return Response({'data': profile_json},
                        status=status.HTTP_200_OK)
    
    @auth_user
    def put(self,request,user_dict):
        profile=UserProfile.objects.get(user=user_dict['id'])
        payload=request.data
        profile_serializer=ProfileSerializer(profile,data=payload,partial=True)
        if profile_serializer.is_valid():
            profile=profile_serializer.save()
            profile_json=profile_serializer.data
            return Response({'data': profile_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(profile_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class AccountHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        user=LoginUser.objects.get(id=user_dict['id'])
        user_json=UserSerializer(user).data
        return Response({'data': user_json},
                        status=status.HTTP_200_OK)
    
    @auth_user
    def put(self,request,user_dict):
        user=LoginUser.objects.get(id=user_dict['id'])
        payload=request.data
        email=payload.get('email',None)
        username=payload.get('username',None)
        first_name=payload.get('first_name',None)
        last_name=payload.get('last_name',None)
        password=payload.get('password',None)
        if email:
            return Response({'Error': "Email cannot be changed"},
                            status=status.HTTP_400_BAD_REQUEST)
        if user.username and username:
            return Response({'Error': "Username cannot be changed more than once"},
                            status=status.HTTP_400_BAD_REQUEST)
        if user.first_name and first_name:
            return Response({'Error': "First name cannot be changed more than once"},
                            status=status.HTTP_400_BAD_REQUEST)
        if user.last_name and last_name:
            return Response({'Error': "Last name cannot be changed more than once"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if password:
            hashed_password=bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt())
            payload['password']=hashed_password
            
        user_serializer=UserSerializer(user,data=payload,partial=True)
        if user_serializer.is_valid():
            user=user_serializer.save()
            user_json=user_serializer.data
            return Response({'data': user_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    def delete(self,request,user_dict):
        user=LoginUser.objects.get(id=user_dict['id'])
        user.delete()
        res=Response({'Message': "Account deleted successfully"},
                        status=status.HTTP_200_OK)
        res.delete_cookie('JWT_TOKEN')
        return res


class CalenderIntegrationHandler(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    @auth_user
    def get(self, request, user_dict, *args, **kwargs):
        integration=Integrations.objects.select_related('user').get(user__id=user_dict['id'])
        if integration.calender_integration is not None:
            params = urlencode({'calender_error': 'true'})
            return redirect(f'{dashboard_url}?{params}')
            
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        dashboard_url = settings.FRONTEND_DASHBOARD_URL

        if error or not code:
            params = urlencode({'calender_error': 'true'})
            return redirect(f'{dashboard_url}?{params}')

        domain = settings.BACKEND_DOMAIN
        api_uri = 'profile/integration/calender'
        redirect_uri = f'{domain}{api_uri}'

        _,refresh_token=google_get_tokens(code=code, redirect_uri=redirect_uri)
        integration.calender_integration=refresh_token
        integration.save()
        
        params=urlencode({'calender_success': 'true'})
        res=redirect(f'{dashboard_url}?{params}')
        return res


class ZoomIntegrationHandler(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
    
    @auth_user
    def get(self,request,user_dict,*args,**kwargs):
        integration=Integrations.objects.select_related('user').get(user__id=user_dict['id'])
        if integration.zoom_integration is not None:
            params = urlencode({'zoom_error': 'true'})
            return redirect(f'{dashboard_url}?{params}')
            
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        dashboard_url = settings.FRONTEND_DASHBOARD_URL

        if error or not code:
            params = urlencode({'zoom_error': 'true'})
            return redirect(f'{dashboard_url}?{params}')
        
        domain = settings.BACKEND_DOMAIN
        api_uri = 'profile/integration/zoom'
        redirect_uri = f'{domain}{api_uri}'
        
        _,refresh_token=get_zoom_tokens(grant_type='authorization_code',token=code,redirect_uri=redirect_uri)
        integration.zoom_integration=refresh_token
        integration.save()
        
        params=urlencode({'zoom_success': 'true'})
        res=redirect(f'{dashboard_url}?{params}')
        return res


class IntegrationHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        integration=Integrations.objects.select_related('user').get(user__id=user_dict['id'])
        integration_json=IntegrationsSerializer(integration).data
        return Response({'data': integration_json},
                        status=status.HTTP_200_OK)