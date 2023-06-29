from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LoginUser
import bcrypt
import jwt
from django.conf import settings
from .serializers import UserSerializer, InputSerializer
from datetime import timedelta
from .decorators import auth_user
from Profile.models import UserProfile
from django.shortcuts import redirect
from urllib.parse import urlencode
from .utils import google_get_tokens, google_get_user_info
from Profile.models import Integrations


class Login(APIView):
    def post(self, request):
        username=request.data.get("username",None)
        password=request.data.get("password",None)
        
        if not username or not password:
            return Response({'Error': "Invalid Username/Password"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user=LoginUser.objects.get(username=username)
        except LoginUser.DoesNotExist:
            return Response({'Error': "Invalid Username/Password"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if not bcrypt.checkpw(str(password).encode('utf-8'), user.password):
            return Response({'Error': "Invalid Username/Password"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        else:
            response={
                'id': user.id
            }
            token=jwt.encode(payload=response,key=settings.JWT_KEY,algorithm=settings.JWT_ALGO)
            token_age=timedelta(days=30).total_seconds()
            res=Response({'Message': "Login Successful"},
                         status=status.HTTP_200_OK)
            res.set_cookie("JWT_TOKEN", token, httponly=True, max_age=token_age)
            return res


class Signup(APIView):
    def post(self,request):
        
        payload=request.data
        password=payload.get('password', None)
        username=payload.get('username', None)
        first_name=payload.get('first_name', None)
        last_name=payload.get('last_name', None)
        if not (password and username and first_name and last_name):
            return Response({'Error': "Invalid form data"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        hashed_password=bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt())
        payload['password']=hashed_password
        
        user_serializer=UserSerializer(data=payload)
        if user_serializer.is_valid():
            user=user_serializer.save()
            response={
                'id': user.id
            }
            token=jwt.encode(payload=response,key=settings.JWT_KEY,algorithm=settings.JWT_ALGO)
            token_age=timedelta(days=30).total_seconds()
            res=Response({'Message': "Signup Successful"},
                         status=status.HTTP_200_OK)
            res.set_cookie("JWT_TOKEN", token, httponly=True, max_age=token_age)
            
            #Setting up profile for user which he/she can edit afterwards
            user_profile=UserProfile.objects.create(user=user)
            user_profile.save()
            #Setting up Integrations
            integration=Integrations.objects.create(user=user)
            integration.save()
            
            return res
        
        else:
            return Response(user_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(APIView):
    def get(self, request, *args, **kwargs):
        input_serializer = InputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = settings.FRONTEND_LOGIN_URL

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        domain = settings.BACKEND_DOMAIN
        api_uri = 'auth/login/google/'
        redirect_uri = f'{domain}{api_uri}'

        access_token, _ = google_get_tokens(code=code, redirect_uri=redirect_uri)
        user_data = google_get_user_info(access_token=access_token)

        profile_data = {
            'email': user_data['email'],
            'first_name': user_data.get('givenName', ''),
            'last_name': user_data.get('familyName', ''),
        }

        # Login and Signup Flow in the same API
        try:
            user=LoginUser.objects.get(email=profile_data['email'])
            response={
                'id': user.id
            }
            token=jwt.encode(payload=response,key=settings.JWT_KEY,algorithm=settings.JWT_ALGO)
            token_age=timedelta(days=30).total_seconds()
            res=redirect(settings.FRONTEND_DASHBOARD_URL)
            res.set_cookie("JWT_TOKEN", token, httponly=True, max_age=token_age)
        
        except LoginUser.DoesNotExist:
            user_serializer=UserSerializer(data=profile_data)
            if user_serializer.is_valid():
                user=user_serializer.save()
                response={
                    'id': user.id
                }
                token=jwt.encode(payload=response,key=settings.JWT_KEY,algorithm=settings.JWT_ALGO)
                token_age=timedelta(days=30).total_seconds()
                res=redirect(settings.FRONTEND_DASHBOARD_URL)
                res.set_cookie("JWT_TOKEN", token, httponly=True, max_age=token_age)
                
                #Setting up profile for user which he/she can edit afterwards
                user_profile=UserProfile.objects.create(user=user)
                user_profile.save()
                #Setting up Integrations
                integration=Integrations.objects.create(user=user)
                integration.save()
            
            else:
                params = urlencode({'error': "Signup failed"})
                res=redirect(f'{login_url}?{params}')
        
        finally:
            return res


class Logout(APIView):
    @auth_user
    def post(self,request,user_dict):
        res=Response({'Message': "Logout Successful"},
                     status=status.HTTP_200_OK)
        res.delete_cookie('JWT_TOKEN')
        return res
