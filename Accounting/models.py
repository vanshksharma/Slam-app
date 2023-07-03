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
    tax=models.IntegerField(null=True)
    amount=models.IntegerField(null=False)
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
    tax=models.IntegerField(null=True)
    amount=models.IntegerField(null=False)
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
    quantity=models.IntegerField(null=False)
    rate=models.IntegerField(null=False)
    amount=models.IntegerField(null=False)
    proposal=models.ForeignKey(Proposal, on_delete=models.CASCADE, db_column="proposal", null=True)
    invoice=models.ForeignKey(Invoice, on_delete=models.CASCADE, db_column="invoice", null=True)
    
    def __str__(self) -> str:
        return f"Details - {self.details} | Amount - {self.amount}"
