from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(models.Model):
    id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=20, null=False)
    last_name=models.CharField(max_length=20, null=False)
    email=models.EmailField(null=False, unique=True)
    phone_no=PhoneNumberField(unique = True, blank = True)
    username=models.CharField(max_length=10, unique=True, null=False)
    password=models.BinaryField(null=False)
    
    def __str__(self) -> str:
        return f"Name - f{self.first_name} f{self.last_name} | Email - f{self.email}"
