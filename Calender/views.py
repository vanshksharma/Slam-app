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
from Profile.models import Integrations
from google.oauth2.credentials import Credentials
from django.conf import settings
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from Profile.models import UserProfile
from Pipeline.models import Contact
from .utils import create_calender_event,update_calender_event,delete_calender_event,make_zoom_meeting,get_zoom_access_token
from django.core.exceptions import PermissionDenied, ValidationError
import time


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
        meeting=request.query_params.get("meeting",None)
        contact=payload.get('contact',None)
        if not contact:
            return Response({'Error':'No Contact Provided'},
                            status=status.HTTP_400_BAD_REQUEST)
        contact=Contact.objects.get(id=contact)
        
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
                diff=due_temp-start_temp
                duration=diff.total_seconds()//60
            except Exception as e:
                return Response({'Error': "Invalid Start or Due provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        payload_serializer=EventSerializer(data=payload)
        if payload_serializer.is_valid():
            # Creating Google Calendar Event
            integration=Integrations.objects.select_related('user').get(user__id=user_dict['id'])
            profile=UserProfile.objects.select_related('user').get(user__id=user_dict['id'])
            calender_success=False
            zoom_success=False
            try:
                creds=Credentials(None,
                            refresh_token=integration.calender_integration,
                            token_uri=settings.GOOGLE_ACCESS_TOKEN_OBTAIN_URL,
                            client_id=settings.GOOGLE_CLIENT_ID,
                            client_secret=settings.GOOGLE_CLIENT_SECRET)
                creds.refresh(Request())
                if creds.valid:
                    calender_service=build('calendar', 'v3', credentials=creds)
                    event= create_calender_event(
                        service=calender_service,
                        summary=payload.get('title',''),
                        description=payload.get('description',''),
                        meeting=meeting,
                        start=start_temp.isoformat(),
                        due=due_temp.isoformat(),
                        timezone=profile.timezone,
                        user_id=user_dict['id'],
                        contact=contact
                    )
                    if event!=-1:
                        calender_success=True
                        payload['calender_event_id']=event.get('id',None)
                        payload['calender_event_link']=event.get('htmlLink',None)
                    
            except:
                integration.calender_integration=None
            
            
            # Zoom Meeting
            if meeting=="true":
                try:
                    access_token,new_refresh_token=get_zoom_access_token(integration.zoom_integration)
                    integration.zoom_integration=new_refresh_token
                    integration.save()
                    join_url=make_zoom_meeting(access_token=access_token,
                                          agenda=payload.get('description',''),
                                          topic=payload.get('title',''),
                                          start_time=start_temp.isoformat(),
                                          timezone=profile.timezone,
                                          invitee=contact.email,
                                          duration=duration)
                    payload['link']=join_url
                    zoom_success=True                    
        
                except PermissionDenied:
                    return Response({'Error':"Zoom Integration Not done. Please Integrate Zoom to create meetings"},
                                    status=status.HTTP_412_PRECONDITION_FAILED)
                except ValidationError:
                    return Response({'Error':"Cannot Create Meeting. Please Try Again Later"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            event_serializer=EventSerializer(data=payload)
            if event_serializer.is_valid():
                event=event_serializer.save()
                event_json=event_serializer.data
                res_payload={'data': event_json}
                res_payload.update({
                    'calender_success':calender_success,
                    'zoom_success':zoom_success
                })
                return Response(res_payload,
                                status=status.HTTP_200_OK)

        else:
            return Response(payload_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
    @auth_user
    @auth_event
    def put(self,request,user_dict,event):
        payload=request.data
        _status=payload.get('status', None)
        start=payload.get('start', None)
        due=payload.get('due', None)
        payload.pop('calender_event_id',None)
        payload.pop('calender_event_link',None)
        payload.pop('link',None)
        
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
        
        payload_serializer=EventSerializer(event, data=payload, partial=True)
        if payload_serializer.is_valid():
            # Updating Google Calendar Event
            try:
                if event.calender_event_id:
                    integration=Integrations.objects.select_related('user').get(user__id=user_dict['id'])
                    update_success=False
                    creds=Credentials(None,
                                refresh_token=integration.calender_integration,
                                token_uri=settings.GOOGLE_ACCESS_TOKEN_OBTAIN_URL,
                                client_id=settings.GOOGLE_CLIENT_ID,
                                client_secret=settings.GOOGLE_CLIENT_SECRET)
                    creds.refresh(Request())
                    if creds.valid:
                        calender_service=build('calendar', 'v3', credentials=creds)
                        new_event= update_calender_event(
                            service=calender_service,
                            event_id=event.calender_event_id,
                            summary=payload.get('title',''),
                            description=payload.get('description',''),
                            start=start,
                            due=due,
                        )
                        if new_event!=-1:
                            update_success=True
                        else:
                            return Response({'Error':"Cannot Update Meeting. Please Try Again Later"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response({'Error':"Calender Integration Expired. Please Connect Calender once more to update Event-1"},
                                    status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                integration.calender_integration=None
                integration.save()
                return Response({'Error':"Calender Integration Expired. Please Connect Calender once more to update Event-2"},
                                    status=status.HTTP_401_UNAUTHORIZED)
            
            finally:
                event_serializer=EventSerializer(event,data=payload,partial=True)
                if event_serializer.is_valid():
                    event=event_serializer.save()
                    event_json=event_serializer.data
                    res_payload={'data': event_json}
                    res_payload.update({
                        'update_success':update_success
                    })
                    return Response(res_payload,
                                    status=status.HTTP_200_OK)
        else:
            return Response(payload_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
                
                
                
    
    @auth_user
    @auth_event
    def delete(self,request,user_dict,event):
        try:
            # Deleting Google Calendar Event
            if event.calender_event_id:
                integration=Integrations.objects.select_related('user').get(user__id=user_dict['id'])
                delete_success=False
                creds=Credentials(None,
                            refresh_token=integration.calender_integration,
                            token_uri=settings.GOOGLE_ACCESS_TOKEN_OBTAIN_URL,
                            client_id=settings.GOOGLE_CLIENT_ID,
                            client_secret=settings.GOOGLE_CLIENT_SECRET)
                creds.refresh(Request())
                if creds.valid:
                    calender_service=build('calendar', 'v3', credentials=creds)
                    res=delete_calender_event(service=calender_service,event_id=event.calender_event_id)
                    if res!=-1:
                        delete_success=True
                    else:
                        return Response({'Error':"Cannot Delete Event. Please Try Again Later"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'Error':"Calender Integration Expired. Please Connect Calender once more to delete Event"},
                                status=status.HTTP_401_UNAUTHORIZED)
        except:
            integration.calender_integration=None
            integration.save()
            return Response({'Error':"Calender Integration Expired. Please Connect Calender once more to delete Event"},
                                status=status.HTTP_401_UNAUTHORIZED)
        finally:
            event.delete()
            return Response({'Message': 'Event Deleted Successfully',
                            'delete_success':delete_success},
                            status=status.HTTP_200_OK)
            