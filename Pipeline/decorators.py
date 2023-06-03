from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Contact, Address, Lead


def auth_contact(func):
    @wraps(func)
    def wrapper(self, request, user_dict, *args, **kwargs):
        contact_id = request.data.get('contact', None)

        if not contact_id:
            return Response({'Error': 'No Contact ID provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            contact = Contact.objects.select_related(
                'user').get(id=contact_id)
        except (Contact.DoesNotExist, ValueError):
            return Response({'Error': "Please Enter Valid Contact ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if contact.user.id != user_dict['id']:
            return Response({'Error': "The Contact does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, contact, *args, **kwargs)

    return wrapper


def auth_address(func):
    @wraps(func)
    def wrapper(self, request, user_dict, *args, **kwargs):
        address_id = request.data.get('address', None)
        if not address_id:
            return Response({'Error': 'No Address ID provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            address = Address.objects.select_related(
                'contact').get(id=address_id)
        except (Address.DoesNotExist, ValueError):
            return Response({'Error': "Please Enter Valid Address ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if address.contact.user.id != user_dict['id']:
            return Response({'Error': "The Address does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, address, *args, **kwargs)

    return wrapper


def auth_lead(func):
    @wraps(func)
    def wrapper(self, request, user_dict, *args, **kwargs):
        lead_id = request.data.get('lead', None)
        if not lead_id:
            return Response({'Error': 'No Lead ID provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            lead = Lead.objects.select_related('contact').get(id=lead_id)
        except Lead.DoesNotExist:
            return Response({'Error': "Please Enter Valid Lead ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if lead.contact.user.id != user_dict['id']:
            return Response({'Error': "The Lead does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, lead, *args, **kwargs)

    return wrapper
