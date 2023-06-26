from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from Auth.decorators import auth_user
from .decorators import auth_project, auth_task
from datetime import date, datetime
from .constants import PriorityConstant, StatusConstant
from Pipeline.models import Contact, Lead
from Pipeline.decorators import auth_contact
from django.db.models import Q


class ProjectHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        projects=Project.objects.select_related('contact').filter(contact__user__id=user_dict['id'])
        project_data=ProjectSerializer(projects, many=True).data
        return Response({'data': project_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_contact
    def post(self,request,user_dict,contact):
        payload=request.data
        payload['created_at']=date.today().isoformat()
        payload['updated_at']=date.today().isoformat()
        priority=payload.get('priority',None)
        start_date=payload.get('start_date',None)
        due_date=payload.get('due_date',None)
        _status=payload.get('status',None)
        lead=payload.get('lead', None)
        
        if lead:
            try:
                lead=Lead.objects.select_related('contact').get(id=lead)
                if lead.contact.user.id != user_dict['id']:
                    return Response({'Error': "The Lead does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Lead.DoesNotExist, ValueError):
                return Response({'Error': "Please Enter Valid Lead ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        
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
                if due_date_temp<start_date_temp:
                        return Response({'Error': "Due date cannot be before Start date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                
            except:
                return Response({'Error': "Invalid Start date or Due date provided"},
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
        start_date=payload.get('start_date',None)
        due_date=payload.get('due_date',None)
        _status=payload.get('status',None)
        lead=payload.get('lead', None)
        
        if lead:
            try:
                lead=Lead.objects.select_related('contact').get(id=lead)
                if lead.contact.user.id != user_dict['id']:
                    return Response({'Error': "The Lead does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Lead.DoesNotExist, ValueError):
                return Response({'Error': "Please Enter Valid Lead ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        
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
                if start_date_temp>project.due_date:
                    return Response({'Error': "Project Start date cannot be after Due Date"},
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
        tasks=Task.objects.select_related('user').filter(user__id=user_dict['id'])
        task_data=TaskSerializer(tasks, many=True).data
        return Response({'data': task_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    def post(self,request,user_dict):
        payload=request.data
        _status=payload.get('status', None)
        priority=payload.get('priority', None)
        date=payload.get('date', None)
        contact=payload.get('contact', None)
        project=payload.get('project', None)
        payload['user']=user_dict['id']
        
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
        
        if project:
            try:
                project=Project.objects.select_related('contact').get(id=project)
                if project.contact.user.id!=user_dict['id']:
                    return Response({'Error': 'Project does not belong to the user'},
                                    status=status.HTTP_403_FORBIDDEN)
                if project.status==StatusConstant.COMPLETE.name:
                    return Response({'Error': "Cannot add task to an already completed project"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if contact:
                    contact=None
                    del payload['contact']
            except:
                return Response({'Error': 'Invalid Project Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        if contact:
            try:
                contact=Contact.objects.select_related('user').get(id=contact)
                if contact.user.id!=user_dict['id']:
                    return Response({'Error': 'Contact does not belong to the user'},
                                        status=status.HTTP_403_FORBIDDEN)
            except:
                return Response({'Error': 'Invalid Contact Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
            
        
        if date:
            try:
                date=datetime.strptime(date, "%Y-%m-%d").date()
                if project:
                    if date<project.start_date:
                        return Response({'Error': "Task date cannot be before Project Start date"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    if date>project.due_date:
                        return Response({'Error': "Task date cannot be after Project Due date"},
                                            status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': 'Invalid Date Provided'},
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
        date=payload.get('date', None)
        contact=payload.get('contact', None)
        project=payload.get('project', None)
        payload['user']=user_dict['id']
        
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
        
        if project:
            try:
                project=Project.objects.select_related('contact').get(id=project)
                if project.contact.user.id!=user_dict['id']:
                    return Response({'Error': 'Project does not belong to the user'},
                                    status=status.HTTP_403_FORBIDDEN)
                if project.status==StatusConstant.COMPLETE.name:
                    return Response({'Error': "Cannot add task to an already completed project"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if task.contact:
                    payload['contact']=None
                if contact:
                    contact=None
            except:
                return Response({'Error': 'Invalid Project Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        if contact:
            try:
                contact=Contact.objects.select_related('user').get(id=contact)
                if contact.user.id!=user_dict['id']:
                    return Response({'Error': 'Contact does not belong to the user'},
                                        status=status.HTTP_403_FORBIDDEN)
                if task.project:
                    payload['project']=None
            except:
                return Response({'Error': 'Invalid Contact Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        
        
        if date and project:
            try:
                date=datetime.strptime(date, "%Y-%m-%d").date()
                if date<project.start_date:
                    return Response({'Error': "Task date cannot be before Project Start date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                if date>project.due_date:
                    return Response({'Error': "Task date cannot be after Project Due date"},
                                        status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': 'Invalid Date Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        elif date and not project:
            try:
                date=datetime.strptime(date, "%Y-%m-%d").date()
                if task.project:
                    if date<task.project.start_date:
                        return Response({'Error': "Task date cannot be before Project Start date"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    if date>task.project.due_date:
                        return Response({'Error': "Task date cannot be after Project Due date"},
                                            status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': 'Invalid Date Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        elif project and not date:
            if task.date<project.start_date:
                return Response({'Error': "Task date cannot be before Project Start date"},
                                            status=status.HTTP_400_BAD_REQUEST)
            if task.date>project.due_date:
                return Response({'Error': "Task date cannot be after Project Due date"},
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
