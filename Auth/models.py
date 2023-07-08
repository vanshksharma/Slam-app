from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class LoginUser(models.Model):
    id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=20, null=False)
    last_name=models.CharField(max_length=20, null=False)
    email=models.EmailField(null=False, unique=True)
    phone_no=PhoneNumberField(unique = True, null=False)
    company=models.CharField(max_length=30,null=True)
    username=models.CharField(max_length=20, unique=True, null=False)
    password=models.BinaryField(null=False,editable=True)
    
    def __str__(self) -> str:
        return f"Name - {self.first_name} {self.last_name} | Email - {self.email}"
