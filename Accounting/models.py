from django.db import models
from Pipeline.models import Contact, Lead
from datetime import date
from Projects.models import Project


class Proposal(models.Model):
    id=models.AutoField(primary_key=True)
    contact=models.ForeignKey(Contact,on_delete=models.CASCADE,db_column="contact")
    proposal_number=models.CharField(max_length=30,null=False)
    creation_date=models.DateField(default=date.today)
    expiry_date=models.DateField()
    lead=models.ForeignKey(Lead, on_delete=models.SET_NULL, db_column="lead", null=True)
    tax=models.FloatField(null=True,default=0)
    amount=models.FloatField(null=False,default=0)
    notes=models.TextField(null=True)
    
    def __str__(self) -> str:
        return f"Amount - {self.amount} | Contact - {self.contact.name}"


class Invoice(models.Model):
    id=models.AutoField(primary_key=True)
    contact=models.ForeignKey(Contact,on_delete=models.CASCADE,db_column="contact")
    invoice_number=models.CharField(max_length=30,null=False)
    creation_date=models.DateField(default=date.today)
    expiry_date=models.DateField()
    project=models.ForeignKey(Project,on_delete=models.SET_NULL,db_column="project",null=True) # Incomplete or Complete
    tax=models.FloatField(null=True,default=0)
    amount=models.FloatField(null=False,default=0)
    notes=models.TextField(null=True)
    
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


class Item(models.Model):
    id=models.AutoField(primary_key=True)
    details=models.CharField(max_length=100, null=False)
    quantity=models.IntegerField(null=False,default=0)
    rate=models.FloatField(null=False,default=0)
    amount=models.FloatField(null=False,default=0)
    proposal=models.ForeignKey(Proposal, on_delete=models.CASCADE, db_column="proposal", null=True)
    invoice=models.ForeignKey(Invoice, on_delete=models.CASCADE, db_column="invoice", null=True)
    
    def __str__(self) -> str:
        return f"Details - {self.details} | Amount - {self.amount}"
