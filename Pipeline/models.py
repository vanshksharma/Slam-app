from django.db import models
from datetime import date
from Auth.models import User
from constants import StageConstant


class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_column="user")
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
        return f"Name - {self.customer_id.name} | City - {self.city}"


class Lead(models.Model):
    id=models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,db_column="customer")
    amount=models.IntegerField(max_length=8,null=True)
    stage=models.CharField(max_length=15,
                           choices=[(tag, tag.value) for tag in StageConstant],
                           default=StageConstant.OPPORTUNITY)
    confidence=models.IntegerField()
    closing_date=models.DateField(null=True,blank=True)
    description=models.TextField(max_length=250,null=True)
    
    class Meta:
        constraints=[
            models.CheckConstraint(check=models.Q(confidence__gte=0) & models.Q(confidence__lte=1),
                                   name="Confidence Range Check",
                                   violation_error_message="Confidence must be between 0 and 1")
        ]
    
    def __str__(self) -> str:
        return f"Customer - {self.customer_id.name} | Stage - {self.stage} "



    
    

