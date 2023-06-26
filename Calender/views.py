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
        start=payload.get('start', None)
        due=payload.get('due', None)
        
        if _status:
            try:
                _status=StatusConstant[_status.upper()]
                payload['status']=_status.name
            except:
                return Response({'Error': 'Invalid Status Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        if start and due:
            try:
                start_temp=datetime.strptime(start, "%Y-%m-%d %H:%M")
                due_temp=datetime.strptime(due, "%Y-%m-%d %H:%M")
                if due_temp<start_temp:
                    return Response({'Error': "Event Due cannot be before Start"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Start or Due provided"},
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
        start=payload.get('start', None)
        due=payload.get('due', None)
        
        if _status:
            try:
                _status=StatusConstant[_status.upper()]
                payload['status']=_status.name
            except:
                return Response({'Error': 'Invalid Status Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        if start and not due:
            try:
                start_temp=datetime.strptime(start, "%Y-%m-%d %H:%M")
                if start_temp>event.due:
                    return Response({'Error': "Event Start cannot be after Due"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Start provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if due and not start:
            try:
                due_temp=datetime.strptime(due, "%Y-%m-%d %H:%M")
                if due_temp<event.start:
                    return Response({'Error': "Event Due cannot be before Start"},
                                        status=status.HTTP_400_BAD_REQUEST)
            
            except:
                return Response({'Error': "Invalid Due provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if start and due:
            try:
                start_temp=datetime.strptime(start, "%Y-%m-%d %H:%M")
                due_temp=datetime.strptime(due, "%Y-%m-%d %H:%M")
                if due_temp<start_temp:
                        return Response({'Error': "Due cannot be before Start"},
                                        status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Start or Due provided"},
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
        