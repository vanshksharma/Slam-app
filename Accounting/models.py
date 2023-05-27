from django.db import models
from Pipeline.models import Lead
from datetime import date
from Projects.models import Project


class Proposal(models.Model):
    id=models.AutoField(primary_key=True)
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE,db_column="lead")
    amount=models.IntegerField(null=False)
    date=models.DateField(default=date.today)
    
    def __str__(self) -> str:
        return f"Amount - {self.amount} | Customer - {self.lead.customer.name}"


class Invoice(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,db_column="project")
    amount=models.IntegerField(null=False)
    date=models.DateField(default=date.today)
    
    def __str__(self) -> str:
        return f"Amount - {self.amount} | Customer - {self.project.lead.customer.name}"


class Payment(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,db_column="project")
    amount_received=models.IntegerField()
    date=models.DateField(default=date.today)
    
    def __str__(self) -> str:
        return f"Amount - {self.amount_received} | Customer - {self.project.lead.customer.name}"
    