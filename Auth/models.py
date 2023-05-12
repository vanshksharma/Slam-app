from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class LoginUser(models.Model):
    id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=20, null=False)
    last_name=models.CharField(max_length=20, null=False)
    email=models.EmailField(null=False, unique=True)
    phone_no=PhoneNumberField(unique = True, blank = True, null=True)
    username=models.CharField(max_length=10, unique=True, null=False)
    password=models.BinaryField(null=False,editable=True)
    
    def __str__(self) -> str:
        return f"Name - {self.first_name} {self.last_name} | Email - {self.email}"
