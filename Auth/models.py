from django.db import models


class LoginUser(models.Model):
    id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=20, null=False, blank=True)
    last_name=models.CharField(max_length=20, null=False, blank=True)
    email=models.EmailField(null=False, unique=True)
    username=models.CharField(max_length=20, unique=True, null=True)
    password=models.BinaryField(null=True,editable=True)
    
    def __str__(self) -> str:
        return f"Name - {self.first_name} {self.last_name} | Email - {self.email}"
