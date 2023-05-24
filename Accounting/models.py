from django.db import models
from Pipeline.models import Lead
from datetime import date


class Proposal(models.Model):
    id=models.AutoField(primary_key=True)
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE,db_column="lead")
    amount=models.IntegerField(null=False)
    date=models.DateField(default=date.today)
    
    def __str__(self) -> str:
        return f"Amount - {self.amount} | Customer - {self.lead.customer.name}"


class Invoice(models.Model):
    id=models.AutoField(primary_key=True)
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE,db_column="lead")
    amount=models.IntegerField(null=False)
    due_date=models.DateField()
    
    def __str__(self) -> str:
        return f"Amount - {self.amount} | Customer - {self.lead.customer.name}"


class Payment(models.Model):
    id=models.AutoField(primary_key=True)
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE)
    amount_received=models.IntegerField()
    date=models.DateField(default=date.today)
    