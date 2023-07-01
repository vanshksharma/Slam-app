from datetime import datetime
import requests
from django.conf import settings
import base64
from django.core.exceptions import PermissionDenied,ValidationError
import json
def create_calender_event(service,summary,description,meeting,start,due,timezone,user_id,contact):
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': timezone if timezone else 'Asia/Kolkata',
        },
        'end': {
            'dateTime': due,
            'timeZone': timezone if timezone else 'Asia/Kolkata',
        },
        'attendees': [
            {'email': contact.email,
             'displayName': contact.name},
        ],
    }
    
    if meeting=='true':
        event.update({
            'conferenceData': {
                'createRequest': {
                    'requestId': user_id
                }
            }
        })
    try:
        new_event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1,sendUpdates='all').execute()
    except:
        new_event=-1
    finally:
        return new_event

def update_calender_event(service,event_id,summary,description,start,due):
    try:
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        event['summary'] = summary if summary else event['summary']
        event['description'] = description if description else event['description']
        event['start']['dateTime'] = datetime.strptime(start, "%Y-%m-%d %H:%M") if start else event['start']['dateTime']
        event['end']['dateTime'] = datetime.strptime(due, "%Y-%m-%d %H:%M") if due else event['end']['dateTime']
        
        updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event,conferenceDataVersion=1,sendUpdates='all').execute()
    
    except:
        updated_event=-1
    finally:
        return updated_event
    
def delete_calender_event(service,event_id):
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True
    except:
        return -1

def get_zoom_access_token(refresh_token):
    username = settings.ZOOM_CLIENT_ID
    password = settings.ZOOM_CLIENT_SECRET
    
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payload={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    response = requests.request("POST", settings.ZOOM_ACCESS_TOKEN_OBTAIN_URL, headers=headers, data=payload)
    if not response.ok:
        raise PermissionDenied
    else:
        return response.json()['access_token'], response.json()['refresh_token']

def make_zoom_meeting(access_token,agenda,start_time,topic,timezone,invitee,duration):
    url=settings.ZOOM_MEETING_URL
    payload = json.dumps({
        "agenda": agenda,
        "default_password": False,
        "start_time": start_time,
        "duration":duration,
        "meeting_invitees": [
            invitee
        ],
        "registrants_confirmation_email": True,
        "registrants_email_notification": True,
        "waiting_room": True,
        "topic": topic,
        "timezone": timezone if timezone else 'Asia/Kolkata',
        "email_notification": True
    })
    
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if not response.ok:
        raise ValidationError("Cannot create meeting")
    else:
        return response.json()['join_url']