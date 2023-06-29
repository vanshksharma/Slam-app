from django.db import models
from datetime import date
from Auth.models import LoginUser
from .constants import StageConstant, TypeConstant
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(LoginUser,on_delete=models.CASCADE,db_column="user")
    contact_type=models.CharField(max_length=20,
                                  choices=[(choice.name, choice.value) for choice in TypeConstant],
                                  default=TypeConstant.INDIVIDUAL.name)
    name=models.CharField(max_length=30,null=False)
    email=models.EmailField(null=False)
    phone_no=PhoneNumberField(unique = True, null=True)
    street=models.CharField(max_length=20,null=True)
    city=models.CharField(max_length=20,null=True)
    state=models.CharField(max_length=20,null=True)
    country=models.CharField(max_length=20,null=True)
    pincode=models.IntegerField(null=True)
    created_at=models.DateField(default=date.today)
    updated_at=models.DateField(default=date.today)
    
    def __str__(self) -> str:
        return f"Name - {self.name} | Email - {self.email}"


class Lead(models.Model):
    id=models.AutoField(primary_key=True)
    contact=models.ForeignKey(Contact,on_delete=models.CASCADE,db_column="contact")
    amount=models.IntegerField(null=True)
    stage=models.CharField(max_length=15,
                           choices=[(choice.name, choice.value) for choice in StageConstant],
                           default=StageConstant.OPPORTUNITY.name)
    confidence=models.FloatField()
    closing_date=models.DateField(null=True,blank=True)
    description=models.TextField(max_length=250,null=True)
    created_at=models.DateField(default=date.today)
    updated_at=models.DateField(default=date.today)
    
    def __str__(self) -> str:
        return f"Contact - {self.contact.name} | Stage - {self.stage}"
