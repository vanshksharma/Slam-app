from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Proposal, Invoice, Payment


def auth_payment(func):
    @wraps(func)
    def wrapper(self, request, user_dict, *args, **kwargs):
        payment_id = request.data.get('payment', None)
        if not payment_id:
            return Response({'Error': 'No Payment ID provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.select_related('lead').get(id=payment_id)
        except Payment.DoesNotExist:
            return Response({'Error': "Please Enter Valid Payment ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if payment.project.lead.customer.user.id != user_dict['id']:
            return Response({'Error': "The Payment does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, payment, *args, **kwargs)

    return wrapper