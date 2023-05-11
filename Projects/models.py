from django.db import models
from Pipeline.models import Lead
from constants import StatusConstant, PriorityConstant
from datetime import date


class Project(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20,null=False)
    value=models.IntegerField(null=False)
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE,db_column="lead")
    priority=models.CharField(max_length=15,
                              choices=[(tag,tag.value) for tag in PriorityConstant],
                              default=PriorityConstant.LOW)
    start_date=models.DateField(default=date.today)
    due_date=models.DateField(null=True)
    status=models.CharField(max_length=15,
                              choices=[(tag,tag.value) for tag in StatusConstant],
                              default=StatusConstant.INCOMPLETE)
    created_at=models.DateField(default=date.today)
    updated_at=models.DateField(default=date.today)
    amount_paid=models.IntegerField(default=0)
    
    class Meta:
        constraints=[
            models.CheckConstraint(check=models.Q(amount_paid__lte=models.F("value")),
                                   name="Amount Paid Check",
                                   violation_error_message="Amount Paid must be less than the value of a project")
        ]
    
    def __str__(self) -> str:
        return f"Name - {self.name} | Customer - {self.lead.customer.name}"


class Task(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20,null=False)
    priority=models.CharField(max_length=15,
                              choices=[(tag,tag.value) for tag in PriorityConstant],
                              default=PriorityConstant.LOW)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,db_column="project")
    status=models.CharField(max_length=15,
                              choices=[(tag,tag.value) for tag in StatusConstant],
                              default=StatusConstant.INCOMPLETE)
    
    def __str__(self) -> str:
        return f"Name - {self.name} | Project - {self.project.name}"

