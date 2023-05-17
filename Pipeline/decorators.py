from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Address, Lead


def auth_customer(func):
    @wraps(func)
    def wrapper(self, request, user_dict, *args, **kwargs):
        if request.method == 'GET':
            customer_id = request.query_params.get('customer', None)
        else:
            customer_id = request.data.get('customer', None)

        if not customer_id:
            return Response({'Error': 'No Customer ID provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.select_related(
                'user').get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({'Error': "Please Enter Valid Customer ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if customer.user.id != user_dict['id']:
            return Response({'Error': "The Customer does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, customer, *args, **kwargs)

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
                'customer').get(id=address_id)
        except Address.DoesNotExist:
            return Response({'Error': "Please Enter Valid Address ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if address.customer.user.id != user_dict['id']:
            return Response({'Error': "The Customer does not belong to the user"},
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
            lead = Lead.objects.select_related('customer').get(id=lead_id)
        except Lead.DoesNotExist:
            return Response({'Error': "Please Enter Valid Lead ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if lead.customer.user.id != user_dict['id']:
            return Response({'Error': "The Lead does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, lead, *args, **kwargs)

    return wrapper
