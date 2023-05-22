from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proposal, Payment, Invoice
from .serializers import ProposalSerializer, PaymentSerializer, InvoiceSerializer
from Auth.decorators import auth_user
from Pipeline.decorators import auth_lead
from .decorators import auth_proposal, auth_invoice
from datetime import date, datetime
from Pipeline.constants import StageConstant
from query_counter.decorators import queries_counter


class ProposalHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        proposals=Proposal.objects.select_related('lead').filter(lead__customer__user__id=user_dict['id'])
        proposal_data=ProposalSerializer(proposals, many=True).data
        return Response({'data': proposal_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_lead
    def post(self,request,user_dict,lead):
        if not (lead.stage==StageConstant.CONTACTED.name or lead.stage==StageConstant.NEGOTIATION.name):
            return Response({'Error': "Proposal can only be added for Contacted or Negotiation stage."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        payload=request.data
        proposal_serializer=ProposalSerializer(data=payload)
        if proposal_serializer.is_valid():
            proposal=proposal_serializer.save()
            proposal_json=proposal_serializer.data
            return Response({'data': proposal_json},
                            status=status.HTTP_200_OK)
        
        else:
            return Response(proposal_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_proposal
    def put(self,request,user_dict,proposal):
        payload=request.data
        proposal_serializer=ProposalSerializer(proposal,data=payload,partial=True)
        if proposal_serializer.is_valid():
            proposal=proposal_serializer.save()
            proposal_json=proposal_serializer.data
            return Response({'data': proposal_json},
                            status=status.HTTP_200_OK)
        
        else:
            return Response(proposal_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_proposal
    def delete(self,request,user_dict,proposal):
        proposal.delete()
        return Response({'Message': 'Proposal Deleted Successfully'},
                        status=status.HTTP_200_OK)


class InvoiceHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        invoices=Invoice.objects.select_related('lead').filter(lead__customer__user__id=user_dict['id'])
        invoice_data=InvoiceSerializer(invoices, many=True).data
        return Response({'data': invoice_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_lead
    def post(self,request,user_dict,lead):
        if not lead.stage==StageConstant.CLOSED_WON.name:
            return Response({'Error': "Invoice can only be generated for Closed Won deals."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        payload=request.data
        invoice_serializer=InvoiceSerializer(data=payload)
        if invoice_serializer.is_valid():
            invoice=invoice_serializer.save()
            invoice_json=invoice_serializer.data
            return Response({'data': invoice_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(invoice_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_invoice
    def put(self,request,user_dict,invoice):
        payload=request.data
        invoice_serializer=InvoiceSerializer(invoice,data=payload,partial=True)
        if invoice_serializer.is_valid():
            invoice=invoice_serializer.save()
            invoice_json=invoice_serializer.data
            return Response({'data': invoice_json},
                            status=status.HTTP_200_OK)
        
        else:
            return Response(invoice_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_invoice
    def delete(self,request,user_dict,invoice):
        invoice.delete()
        return Response({'Message': 'Invoice Deleted Successfully'},
                        status=status.HTTP_200_OK)