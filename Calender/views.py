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
        
        if _status:
            try:
                _status=StatusConstant[_status.upper()]
                payload['status']=_status.name
            except:
                return Response({'Error': 'Invalid Status Provided'},
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
        date=payload.get('date')
        
        if _status:
            try:
                _status=StatusConstant[_status.upper()]
                payload['status']=_status.name
            except:
                return Response({'Error': 'Invalid Status Provided'},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        if date:
            try:
                date=datetime.strptime(date, '%Y-%m-%d').date()
                if date<event.contact.created_at:
                    return Response({'Error': "Event creation date cannot be before Contact Creation date"},
                                    status=status.HTTP_400_BAD_REQUEST)
            
            except:
                return Response({'Error': "Enter Valid Closing Date"},
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
        