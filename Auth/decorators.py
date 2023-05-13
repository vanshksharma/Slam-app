from functools import wraps
import jwt
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


def auth_user(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        token=request.headers.get('token', None)
        if not token:
            return Response({'Error': "Forbidden"},
                            status=status.HTTP_403_FORBIDDEN)
        
        try:
            user_dict=jwt.decode(token,key=settings.JWT_KEY,algorithms=[settings.JWT_ALGO])
        except:
            return Response({'Error': "Invalid Token"},
                            status=status.HTTP_403_FORBIDDEN)
        
        return func(self,request,user_dict,*args,**kwargs)
    
    return wrapper