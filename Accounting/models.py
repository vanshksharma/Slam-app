from django.db import models
from Pipeline.models import Contact, Lead
from datetime import date
from Projects.models import Project


class Proposal(models.Model):
    id=models.AutoField(primary_key=True)
    contact=models.ForeignKey(Contact,on_delete=models.CASCADE,db_column="contact")      
    amount=models.IntegerField(null=False)
    date=models.DateField(default=date.today)
    lead=models.ForeignKey(Lead, on_delete=models.SET_NULL, db_column="lead", null=True)
    
    def __str__(self) -> str:
        return f"Amount - {self.amount} | Contact - {self.contact.name}"


class Invoice(models.Model):
    id=models.AutoField(primary_key=True)
    contact=models.ForeignKey(Contact,on_delete=models.CASCADE,db_column="contact")
    amount=models.IntegerField(null=False)
    date=models.DateField(default=date.today)
    project=models.ForeignKey(Project,on_delete=models.SET_NULL,db_column="project",null=True) # Incomplete or Complete
    
    def __str__(self) -> str:
        return f"Amount - {self.amount} | Contact - {self.contact.name}"


class Payment(models.Model):
    id=models.AutoField(primary_key=True)
    contact=models.ForeignKey(Contact,on_delete=models.CASCADE,db_column="contact")
    amount_received=models.IntegerField()
    date=models.DateField(default=date.today)
    project=models.ForeignKey(Project,on_delete=models.SET_NULL,db_column="project",null=True) # Incomplete or Complete
    
    def __str__(self) -> str:
        return f"Amount - {self.amount_received} | Contact - {self.contact.name}"
    