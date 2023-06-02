from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Auth.decorators import auth_user
from .models import UserProfile
from .serializers import ProfileSerializer
from Auth.models import LoginUser
from Auth.serializers import UserSerializer
import bcrypt
# No Post and Delete API'S because profile gets automatically created at the time of signup and user cannot delete a profile, he/she can only delete the account.


class ProfileHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        print(user_dict)
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
    