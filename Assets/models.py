from django.db import models
from Auth.models import LoginUser
from datetime import date
from Projects.models import Project


class Asset(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(LoginUser, on_delete=models.CASCADE, db_column='user')
    url=models.URLField(null=False)
    created_at=models.DateField(default=date.today)
    updated_at=models.DateField(default=date.today)
    project=models.ForeignKey(Project, on_delete=models.SET_NULL, db_column='project',null=True)
    filename=models.CharField(max_length=100, null=False)
    