from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Proposal, Invoice


def auth_proposal(func):
    @wraps(func)
    def wrapper(self, request, user_dict, *args, **kwargs):
        proposal_id = request.data.get('proposal', None)
        if not proposal_id:
            return Response({'Error': 'No Proposal ID provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            proposal = Proposal.objects.select_related('lead').get(id=proposal_id)
        except Proposal.DoesNotExist:
            return Response({'Error': "Please Enter Valid Proposal ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if proposal.lead.customer.user.id != user_dict['id']:
            return Response({'Error': "The Proposal does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, proposal, *args, **kwargs)

    return wrapper

def auth_invoice(func):
    @wraps(func)
    def wrapper(self, request, user_dict, *args, **kwargs):
        invoice_id = request.data.get('invoice', None)
        if not invoice_id:
            return Response({'Error': 'No Invoice ID provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            invoice = Invoice.objects.select_related('lead').get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response({'Error': "Please Enter Valid Invoice ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if invoice.lead.customer.user.id != user_dict['id']:
            return Response({'Error': "The Invoice does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, invoice, *args, **kwargs)

    return wrapper