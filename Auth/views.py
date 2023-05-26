from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LoginUser
import bcrypt
import jwt
from django.conf import settings
from .serializers import UserSerializer
from datetime import timedelta
from .decorators import auth_user
from Profile.models import UserProfile


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
        if not password:
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
            user_profile=UserProfile.objects.create(user=user.id)
            user_profile.save()
            
            return res
        
        else:
            return Response(user_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    @auth_user
    def post(self,request,user_dict):
        res=Response({'Message': "Logout Successful"},
                     status=status.HTTP_200_OK)
        res.delete_cookie('JWT_TOKEN')
        return res
