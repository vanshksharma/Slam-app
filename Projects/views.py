from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from Auth.decorators import auth_user
from .decorators import auth_project
from datetime import date, datetime
from Pipeline.decorators import auth_lead
from .constants import PriorityConstant, StatusConstant
from Pipeline.constants import StageConstant
from query_counter.decorators import queries_counter
from django.db.models import Sum


class ProjectHandler(APIView):
    @auth_user
    @queries_counter
    def get(self,request,user_dict):
        projects=Project.objects.select_related('lead').filter(lead__customer__user__id=user_dict['id'])
        project_data=ProjectSerializer(projects, many=True).data
        return Response({'data': project_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_lead
    def post(self,request,user_dict,lead):
        payload=request.data
        payload['created_at']=date.today().isoformat()
        payload['updated_at']=date.today().isoformat()
        
        if not (lead.stage==StageConstant.CLOSED_WON.name):
            return Response({'Error':"Projects can be added only in Closed_Won stage"},
                            status=status.HTTP_403_FORBIDDEN)
        
        priority=payload.get('priority',None)
        value=payload.get('value',None)
        start_date=payload.get('start_date',None)
        due_date=payload.get('due_date',None)
        _status=payload.get('status',None)
        amount_paid=payload.get('amount_paid',None)
        
        if priority:
            try:
                priority=PriorityConstant[priority.upper()]
                payload['priority']=priority.name
            except:
                return Response({'Error': 'Invalid Priority Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if _status:
            try:
                _status=StatusConstant[_status.upper()]
                payload['status']=_status.name
            except:
                return Response({'Error': 'Invalid Status Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if amount_paid and value:
                try:
                    if int(amount_paid)>int(value):
                        return Response({'Error': "Amount paid cannot be greater than the value of the project"},
                                        status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({'Error': "Invalid amount_paid or value provided"})
        
        if start_date:
            try:
                start_date_temp=datetime.strptime(start_date, "%Y-%m-%d").date()
                if start_date_temp<date.today():
                        return Response({'Error': "Invalid Start date provided"})
            except:
                return Response({'Error': "Invalid Start date provided"})
        
        if due_date:
            if start_date:
                try:
                    start_date=datetime.strptime(start_date, "%Y-%m-%d").date()
                    due_date=datetime.strptime(due_date, "%Y-%m-%d").date()
                    if due_date<start_date:
                        return Response({'Error': "Due date cannot be before Start date"})
                except:
                    return Response({'Error': "Invalid Start date or Due date provided"})
            
            else:
                try:
                    due_date=datetime.strptime(due_date, "%Y-%m-%d").date()
                    if due_date<date.today():
                        return Response({'Error': "Due date cannot be before Start date"})
                except:
                    return Response({'Error': "Invalid Due date provided"})
        
        #Checking if this project value is valid corresponding to the lead
        if value:
            total_projects_value=Project.objects.select_related('lead').filter(lead__id=lead.id).aggregate(tot_value=Sum('value')).get('tot_value',0)
            if total_projects_value:
                if lead.amount<total_projects_value+value:
                    return Response({'Error': "Combined Project values exceeding the lead amount"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                if lead.amount<value:
                    return Response({'Error': "Project value exceeds the lead amount"},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        project_serializer=ProjectSerializer(data=payload)
        if project_serializer.is_valid():
            project=project_serializer.save()
            project_json=project_serializer.data
            return Response({'data': project_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(project_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_project
    def put(self,request,user_dict,project):
        payload=request.data
        if 'created_at' in payload:
            del payload['created_at']
        
        priority=payload.get('priority',None)
        value=payload.get('value',None)
        start_date=payload.get('start_date',None)
        due_date=payload.get('due_date',None)
        _status=payload.get('status',None)
        amount_paid=payload.get('amount_paid',None)
        
        if priority:
            try:
                priority=PriorityConstant[priority.upper()]
                payload['priority']=priority.name
            except:
                return Response({'Error': 'Invalid Priority Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if _status:
            try:
                _status=StatusConstant[_status.upper()]
                payload['status']=_status.name
            except:
                return Response({'Error': 'Invalid Status Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if amount_paid:
            if value:
                try:
                    if int(amount_paid)>int(value):
                        return Response({'Error': "Amount paid cannot be greater than the value of the project"},
                                        status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({'Error': "Invalid amount_paid or value provided"})
            
            else:
                try:
                    if int(amount_paid)>project.value:
                        return Response({'Error': "Amount paid cannot be greater than the value of the project"},
                                        status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({'Error': "Invalid amount_paid provided"})
        
        if start_date:
            try:
                start_date_temp=datetime.strptime(start_date, "%Y-%m-%d").date()
                if start_date_temp<project.created_at:
                        return Response({'Error': "Start date cannot be less than the date on which project was created"})
            except:
                return Response({'Error': "Invalid Start date provided"})
                
        if due_date:
            if start_date:
                try:
                    start_date=datetime.strptime(start_date, "%Y-%m-%d").date()
                    due_date=datetime.strptime(due_date, "%Y-%m-%d").date()
                    if due_date<start_date:
                        return Response({'Error': "Due date cannot be before Start date"})
                except:
                    return Response({'Error': "Invalid Start date or Due date provided"})
            
            else:
                try:
                    due_date=datetime.strptime(due_date, "%Y-%m-%d").date()
                    if due_date<project.start_date:
                        return Response({'Error': "Due date cannot be before Start date"})
                except:
                    return Response({'Error': "Invalid Due date provided"})
        
        #Checking if this project value is valid corresponding to the lead
        if value:
            try:
                value=int(value)
            except:
                return Response({'Error': "Invalid value provided"})
            if value<project.amount_paid:
                return Response({'Error': "Value cannot be less than the amount_paid for the project"})
            total_projects_value=Project.objects.select_related('lead').filter(lead__id=project.lead.id).exclude(id=project.id).aggregate(tot_value=Sum('value')).get('tot_value',0)
            if total_projects_value:
                if project.lead.amount<total_projects_value+value:
                    return Response({'Error': "Combined Project values exceeding the lead amount"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                if project.lead.amount<value:
                    return Response({'Error': "Project value exceeds the lead amount"},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        payload['updated_at']=date.today().isoformat()
        project_serializer=ProjectSerializer(project,data=payload,partial=True)
        if project_serializer.is_valid():
            project=project_serializer.save()
            project_json=project_serializer.data
            return Response({'data': project_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(project_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_project
    def delete(self,request,user_dict,project):
        project.delete()
        return Response({'Message': 'Project Deleted Successfully'},
                        status=status.HTTP_200_OK)