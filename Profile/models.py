from django.db import models
from Auth.models import LoginUser
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField


class UserProfile(models.Model):
    user=models.OneToOneField(LoginUser,primary_key=True,on_delete=models.CASCADE,db_column="user")
    legal_name=models.CharField(max_length=20,null=True)
    entity=models.CharField(max_length=10, null=True)
    country=models.CharField(max_length=20,null=True)
    state=models.CharField(max_length=20, null=True)
    currency=models.CharField(max_length=10, null=True)
    timezone=TimeZoneField(null=True)
    address=models.TextField(max_length=50,null=True)
    city=models.CharField(max_length=20,null=True)
    pincode=models.IntegerField(null=True)
    phone_no=PhoneNumberField(unique = True, null=True)
    
    
    
    
    
    
    
