from django.db import models
from Pipeline.models import Lead
from datetime import date
from Pipeline.constants import StageConstant
from Projects.models import Project


class Proposal(models.Model):
    id=models.AutoField(primary_key=True)
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE,db_column="lead")
    amount=models.IntegerField(max_length=8,null=False)
    date=models.DateField(default=date.today)
    
    class Meta:
        constraints=[
            models.CheckConstraint(check=~(models.Q(lead__stage=StageConstant.OPPORTUNITY) | models.Q(lead__stage=StageConstant.CLOSED_LOST)),
                                   name="Lead Stage Check",
                                   violation_error_message="Lead must be in Contacted or Negotiation stage to generate a Proposal")
        ]
    
    def __str__(self) -> str:
        return f"Amount - f{self.amount} | Customer - f{self.lead.customer.name}"


class Invoice(models.Model):
    id=models.AutoField(primary_key=True)
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE,db_column="lead")
    amount=models.IntegerField(max_length=8,null=False)
    due_date=models.DateField()
    
    class Meta:
        constraints=[
            models.CheckConstraint(check=models.Q(lead__stage=StageConstant.CLOSED_WON),
                                   name="Lead Stage Check",
                                   violation_error_message="Lead must be in Closed Won stage to generate an Invoice")
        ]
    
    def __str__(self) -> str:
        return f"Amount - f{self.amount} | Customer - f{self.lead.customer.name}"


class Payment(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    amount_received=models.IntegerField()
    