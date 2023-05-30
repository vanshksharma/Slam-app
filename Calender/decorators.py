from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Event


def auth_event(func):
    @wraps(func)
    def wrapper(self, request, user_dict, *args, **kwargs):
        event_id = request.data.get('event', None)

        if not event_id:
            return Response({'Error': 'No Event ID provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.select_related(
                'contact').get(id=event_id)
        except Event.DoesNotExist:
            return Response({'Error': "Please Enter Valid Event ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if event.contact.user.id != user_dict['id']:
            return Response({'Error': "The Event does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, event, *args, **kwargs)

    return wrapper