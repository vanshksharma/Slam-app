from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Pipeline.decorators import auth_contact
from Auth.decorators import auth_user
from Projects.constants import StatusConstant
from .models import Event
from .serializers import EventSerializer
from datetime import datetime
from .decorators import auth_event


class EventHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        events=Event.objects.select_related('contact').filter(contact__user__id=user_dict['id'])
        event_data=EventSerializer(events, many=True).data
        return Response({'data': event_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_contact
    def post(self,request,user_dict,contact):
        payload=request.data
        _status=payload.get('status', None)
        start_date=payload.get('start_date', None)
        due_date=payload.get('due_date', None)
        
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
        
        event_serializer=EventSerializer(data=payload)
        if event_serializer.is_valid():
            event=event_serializer.save()
            event_json=event_serializer.data
            return Response({'data': event_json},
                            status=status.HTTP_200_OK)

        else:
            return Response(event_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
    @auth_user
    @auth_event
    def put(self,request,user_dict,event):
        payload=request.data
        _status=payload.get('status', None)
        start_date=payload.get('start_date', None)
        due_date=payload.get('due_date', None)
        
        if _status:
            try:
                _status=StatusConstant[_status.upper()]
                payload['status']=_status.name
            except:
                return Response({'Error': 'Invalid Status Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        if start_date and not due_date:
            try:
                start_date_temp=datetime.strptime(start_date, "%Y-%m-%d").date()
                if start_date_temp>event.due_date:
                    return Response({'Error': "Task Start date cannot be after Due date"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Start date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if due_date and not start_date:
            try:
                due_date_temp=datetime.strptime(due_date, "%Y-%m-%d").date()
                if due_date_temp<event.start_date:
                    return Response({'Error': "Task Due date cannot be before Start date"},
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
            except:
                return Response({'Error': "Invalid Start date or Due date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        event_serializer=EventSerializer(event, data=payload, partial=True)
        if event_serializer.is_valid():
            event=event_serializer.save()
            event_json=event_serializer.data
            return Response({'data': event_json},
                            status=status.HTTP_200_OK)

        else:
            return Response(event_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_event
    def delete(self,request,user_dict,event):
        event.delete()
        return Response({'Message': 'Event Deleted Successfully'},
                        status=status.HTTP_200_OK)
        