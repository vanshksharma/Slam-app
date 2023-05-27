from django.db import models
from datetime import date
from Auth.models import LoginUser
from .constants import StageConstant


class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(LoginUser,on_delete=models.CASCADE,db_column="user")
    customer_type=models.CharField(max_length=20,null=False)
    name=models.CharField(max_length=20,null=False)
    email=models.EmailField(unique=True,null=False)
    created_at=models.DateField(default=date.today)
    updated_at=models.DateField(default=date.today)
    
    def __str__(self) -> str:
        return f"Name - {self.name} | Email - {self.email}"
    

class Address(models.Model):
    id=models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,db_column="customer")
    street=models.CharField(max_length=20,null=False)
    city=models.CharField(max_length=20,null=False)
    state=models.CharField(max_length=20,null=False)
    country=models.CharField(max_length=20,null=False)
    pincode=models.BigIntegerField(null=False)
    created_at=models.DateField(default=date.today)
    updated_at=models.DateField(default=date.today)
    
    def __str__(self) -> str:
        return f"Name - {self.customer.name} | City - {self.city}"


class Lead(models.Model):
    id=models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,db_column="customer")
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
        return f"Customer - {self.customer.name} | Stage - {self.stage}"



    
    

