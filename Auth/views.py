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
from django.db.models import Q
from django.core.exceptions import ValidationError


class Login(APIView):
    def post(self, request):
        username=request.data.get("username",None)
        password=request.data.get("password",None)
        
        if not username or not password:
            return Response({'Error': "Invalid Username/Password"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user=LoginUser.objects.get(Q(username=username)| Q(email=username))
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
            res.set_cookie("JWT_TOKEN", token, httponly=True, max_age=token_age,samesite='None',secure=True)
            return res


class Signup(APIView):
    def post(self,request):
        payload=request.data
        password=payload.get('password', None)
        username=payload.get('username', None)
        first_name=payload.get('first_name', None)
        last_name=payload.get('last_name', None)
        email=payload.get('email', None)
        phone_no=payload.get('phone_no', None)
        if not (password and username and first_name and last_name and email and phone_no):
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
            res.set_cookie("JWT_TOKEN", token, httponly=True, max_age=token_age,samesite='None',secure=True)
            
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

        try:
            access_token, _ = google_get_tokens(code=code, redirect_uri=redirect_uri)
            user_data = google_get_user_info(access_token=access_token)
        
        except ValidationError:
            params=urlencode({'error':'true'})
            res=redirect(f'{login_url}?{params}')
        
        try:
            user=LoginUser.objects.get(email=user_data['email'])
            response={
                'id': user.id
            }
            token=jwt.encode(payload=response,key=settings.JWT_KEY,algorithm=settings.JWT_ALGO)
            token_age=timedelta(days=30).total_seconds()
            res=redirect(settings.FRONTEND_DASHBOARD_URL)
            res.set_cookie("JWT_TOKEN", token, httponly=True, max_age=token_age,samesite='None',secure=True)
        
        except LoginUser.DoesNotExist:
            params=urlencode({'error':'true'})
            res=redirect(f'{login_url}?{params}')
            
        finally:
            return res


class GoogleSignup(APIView):
    def get(self, request, *args, **kwargs):
        input_serializer = InputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        signup_url = settings.FRONTEND_SIGNUP_URL

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{signup_url}?{params}')

        domain = settings.BACKEND_DOMAIN
        api_uri = 'auth/signup/google/'
        redirect_uri = f'{domain}{api_uri}'

        try:
            access_token, _ = google_get_tokens(code=code, redirect_uri=redirect_uri)
            user_data = google_get_user_info(access_token=access_token)
        
        except ValidationError:
            params=urlencode({'error':'true'})
            res=redirect(f'{signup_url}?{params}')
            
        params=urlencode({'email':user_data['email']})
        res=redirect(f'{signup_url}?{params}')
        return res

class Logout(APIView):
    @auth_user
    def post(self,request,user_dict):
        res=Response({'Message': "Logout Successful"},
                     status=status.HTTP_200_OK)
        res.delete_cookie('JWT_TOKEN')
        return res
