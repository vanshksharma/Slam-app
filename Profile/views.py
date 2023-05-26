from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Auth.decorators import auth_user
from query_counter.decorators import queries_counter
from .models import UserProfile
from .serializers import ProfileSerializer
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
        