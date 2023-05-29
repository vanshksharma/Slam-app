from django.db import models
from Pipeline.models import Contact
from datetime import date
from Projects.constants import StatusConstant


class Event(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=20,null=False)
    contact=models.ForeignKey(Contact,on_delete=models.CASCADE,db_column="contact")
    description=models.TextField(max_length=250,null=True)
    date=models.DateField(default=date.today)
    status=models.CharField(max_length=15,
                              choices=[(tag.name,tag.value) for tag in StatusConstant],
                              default=StatusConstant.INCOMPLETE.name)
    link=models.URLField(null=True)