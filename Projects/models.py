from django.db import models
from Pipeline.models import Contact, Lead
from .constants import StatusConstant, PriorityConstant
from datetime import date


class Project(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20,null=False)
    value=models.IntegerField(null=False)
    contact=models.ForeignKey(Contact,on_delete=models.CASCADE,db_column="contact")
    priority=models.CharField(max_length=15,
                              choices=[(tag.name,tag.value) for tag in PriorityConstant],
                              default=PriorityConstant.LOW.name)
    start_date=models.DateField()
    due_date=models.DateField()
    status=models.CharField(max_length=15,
                              choices=[(tag.name,tag.value) for tag in StatusConstant],
                              default=StatusConstant.INCOMPLETE.name)
    created_at=models.DateField(default=date.today)
    updated_at=models.DateField(default=date.today)
    lead=models.ForeignKey(Lead, on_delete=models.SET_NULL, db_column="lead", null=True)
    
    def __str__(self) -> str:
        return f"Name - {self.name} | Contact - {self.contact.name}"


class Task(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20,null=False)
    priority=models.CharField(max_length=15,
                              choices=[(tag.name,tag.value) for tag in PriorityConstant],
                              default=PriorityConstant.LOW.name)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,db_column="project")
    status=models.CharField(max_length=15,
                              choices=[(tag.name,tag.value) for tag in StatusConstant],
                              default=StatusConstant.INCOMPLETE.name)
    start_date=models.DateField()
    due_date=models.DateField()
    
    def __str__(self) -> str:
        return f"Name - {self.name} | Project - {self.project.name}"

