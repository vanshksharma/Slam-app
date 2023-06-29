from datetime import datetime

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