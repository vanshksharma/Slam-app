from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from Auth.decorators import auth_user
from .decorators import auth_project, auth_task
from datetime import date, datetime
from Pipeline.decorators import auth_lead
from .constants import PriorityConstant, StatusConstant
from Pipeline.constants import StageConstant
from query_counter.decorators import queries_counter
from django.db.models import Sum, Q


class ProjectHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        projects=Project.objects.select_related('lead').filter(lead__customer__user__id=user_dict['id'])
        project_data=ProjectSerializer(projects, many=True).data
        return Response({'data': project_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_lead
    def post(self,request,user_dict,lead):
        if not (lead.stage==StageConstant.CLOSED_WON.name):
            return Response({'Error':"Projects can be added only in Closed_Won stage"},
                            status=status.HTTP_403_FORBIDDEN)
            
        payload=request.data
        payload['created_at']=date.today().isoformat()
        payload['updated_at']=date.today().isoformat()
        
        priority=payload.get('priority',None)
        value=payload.get('value',None)
        start_date=payload.get('start_date',None)
        due_date=payload.get('due_date',None)
        _status=payload.get('status',None)
        
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
        
        if start_date and due_date:
            try:
                start_date_temp=datetime.strptime(start_date, "%Y-%m-%d").date()
                due_date_temp=datetime.strptime(due_date, "%Y-%m-%d").date()
                if start_date_temp<lead.closing_date:
                        return Response({'Error': "Project Start date cannot be before Lead Closing date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                if due_date_temp<start_date_temp:
                        return Response({'Error': "Due date cannot be before Start date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                
            except:
                return Response({'Error': "Invalid Start date or Due date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        #Checking if this project value is valid corresponding to the lead
        if value:
            try:
                value=int(value)
                total_projects_value=Project.objects.select_related('lead').filter(lead__id=lead.id).aggregate(tot_value=Sum('value')).get('tot_value',0)
                if total_projects_value:
                    if lead.amount<total_projects_value+value:
                        return Response({'Error': "Combined Project values exceeding the lead amount"},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    if lead.amount<value:
                        return Response({'Error': "Project value exceeds the lead amount"},
                                        status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid value provided"},
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
                if _status==StatusConstant.COMPLETE:
                    incomplete_tasks=Task.objects.select_related('project').filter(project__id=project.id, status=StatusConstant.INCOMPLETE.name).count()
                    if incomplete_tasks>0:
                        return Response({'Error': "Complete all the tasks before marking the project as Complete"},
                                        status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': 'Invalid Status Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if start_date and not due_date:
            try:
                start_date_temp=datetime.strptime(start_date, "%Y-%m-%d").date()
                if start_date_temp<project.lead.closing_date:
                        return Response({'Error': "Project start date cannot be before Lead closing date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                if start_date_temp>project.due_date:
                    return Response({'Error': "Due date cannot be before Start date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                tasks_before_new_start_date=Task.objects.select_related('project').filter(Q(project__id=project.id) & Q(start_date__lt=start_date_temp)).count()
                if tasks_before_new_start_date>0:
                    return Response({'Error': "Project contains Tasks with start date before the start date of Project"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Start date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if due_date and not start_date:
            try:
                due_date_temp=datetime.strptime(due_date, "%Y-%m-%d").date()
                if due_date_temp<project.start_date:
                    return Response({'Error': "Project Due date cannot be before Start date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                tasks_after_new_due_date=Task.objects.select_related('project').filter(Q(project__id=project.id) & Q(due_date__gt=due_date_temp)).count()
                if tasks_after_new_due_date>0:
                    return Response({'Error': "Project contains Tasks with Due date after the Due date of Project"},
                                    status=status.HTTP_400_BAD_REQUEST)
            
            except:
                return Response({'Error': "Invalid Due date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if start_date and due_date:
            try:
                start_date_temp=datetime.strptime(start_date, "%Y-%m-%d").date()
                due_date_temp=datetime.strptime(due_date, "%Y-%m-%d").date()
                if start_date_temp<project.lead.closing_date:
                        return Response({'Error': "Project Start date cannot be before Lead Closing date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                if due_date_temp<start_date_temp:
                        return Response({'Error': "Due date cannot be before Start date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                tasks_after_new_due_date_and_before_new_start_date=Task.objects.select_related('project').filter(Q(project__id=project.id) & (Q(due_date__gt=due_date_temp) | Q(start_date__lt=start_date_temp))).count()
                if tasks_after_new_due_date_and_before_new_start_date>0:
                    return Response({'Error': "Project contains Tasks with Due date after the Due date of Project or with Start date before the Start date of Project"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Start date or Due date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        #Checking if this project value is valid corresponding to the lead
        if value:
            try:
                value=int(value)
                total_projects_value=Project.objects.select_related('lead').filter(lead__id=project.lead.id).exclude(id=project.id).aggregate(tot_value=Sum('value')).get('tot_value',0)
                if total_projects_value:
                    if project.lead.amount<total_projects_value+value:
                        return Response({'Error': "Combined Project values exceeding the lead amount"},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    if project.lead.amount<value:
                        return Response({'Error': "Project value exceeds the lead amount"},
                                        status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid value provided"},
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


class TaskHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        tasks=Task.objects.select_related('project').filter(project__lead__customer__user__id=user_dict['id'])
        task_data=TaskSerializer(tasks, many=True).data
        return Response({'data': task_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_project
    def post(self,request,user_dict,project):
        if project.status==StatusConstant.COMPLETE.name:
            return Response({'Error': "Cannot add task to an already completed project"},
                            status=status.HTTP_400_BAD_REQUEST)
        payload=request.data
        _status=payload.get('status', None)
        priority=payload.get('priority', None)
        start_date=payload.get('start_date', None)
        due_date=payload.get('due_date', None)
        
        if _status:
            try:
                _status=StatusConstant[_status.upper()]
                payload['status']=_status.name
            except:
                return Response({'Error': 'Invalid Status Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        if priority:
            try:
                priority=PriorityConstant[priority.upper()]
                payload['priority']=priority.name
            except:
                return Response({'Error': 'Invalid Priority Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        if start_date and due_date:
            try:
                start_date_temp=datetime.strptime(start_date, "%Y-%m-%d").date()
                due_date_temp=datetime.strptime(due_date, "%Y-%m-%d").date()
                if start_date_temp<project.start_date:
                    return Response({'Error': "Task Start date cannot be before Project Start date"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if due_date_temp>project.due_date:
                    return Response({'Error': "Task Due date cannot be after Project Due date"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if due_date_temp<start_date_temp:
                    return Response({'Error': "Due date cannot be before Start date"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Start date or Due date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
            
            
        task_serializer=TaskSerializer(data=payload)
        if task_serializer.is_valid():
            task=task_serializer.save()
            task_json=task_serializer.data
            return Response({'data': task_json},
                            status=status.HTTP_200_OK)
        
        else:
            return Response(task_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_task
    def put(self,request,user_dict,task):
        payload=request.data
        _status=payload.get('status', None)
        priority=payload.get('priority', None)
        start_date=payload.get('start_date', None)
        due_date=payload.get('due_date', None)
        
        if _status:
            try:
                _status=StatusConstant[_status.upper()]
                payload['status']=_status.name
            except:
                return Response({'Error': 'Invalid Status Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
            
            if _status==StatusConstant.INCOMPLETE:
                if task.project.status==StatusConstant.COMPLETE.name:
                    return Response({'Error': "Cannot mark the task of an already completed project as Incomplete"},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        if priority:
            try:
                priority=PriorityConstant[priority.upper()]
                payload['priority']=priority.name
            except:
                return Response({'Error': 'Invalid Priority Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        
        if start_date and not due_date:
            try:
                start_date_temp=datetime.strptime(start_date, "%Y-%m-%d").date()
                if start_date_temp<task.project.start_date:
                    return Response({'Error': "Task Start date cannot be before Project Start date"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if start_date_temp>task.due_date:
                    return Response({'Error': "Task Start date cannot be after Due date"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Start date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if due_date and not start_date:
            try:
                due_date_temp=datetime.strptime(due_date, "%Y-%m-%d").date()
                if due_date_temp>task.project.due_date:
                    return Response({'Error': "Task Due date cannot be after Project Due date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                if due_date_temp<task.start_date:
                    return Response({'Error': "Task Due date cannot be before Start date"},
                                        status=status.HTTP_400_BAD_REQUEST)
            
            except:
                return Response({'Error': "Invalid Due date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if start_date and due_date:
            try:
                start_date_temp=datetime.strptime(start_date, "%Y-%m-%d").date()
                due_date_temp=datetime.strptime(due_date, "%Y-%m-%d").date()
                if start_date_temp<task.project.start_date:
                    return Response({'Error': "Task Start date cannot be before Project Start date"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if due_date_temp>task.project.due_date:
                    return Response({'Error': "Task Due date cannot be after Project Due date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                if due_date_temp<start_date_temp:
                        return Response({'Error': "Due date cannot be before Start date"},
                                        status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Start date or Due date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        task_serializer=TaskSerializer(task,data=payload,partial=True)
        if task_serializer.is_valid():
            task=task_serializer.save()
            task_json=task_serializer.data
            return Response({'data': task_json},
                            status=status.HTTP_200_OK)
        
        else:
            return Response(task_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_task
    def delete(self,request,user_dict,task):
        task.delete()
        return Response({'Message': 'Task Deleted Successfully'},
                        status=status.HTTP_200_OK)
