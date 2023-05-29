from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proposal, Payment, Invoice
from .serializers import ProposalSerializer, PaymentSerializer, InvoiceSerializer
from Auth.decorators import auth_user
from Pipeline.decorators import auth_lead
from .decorators import auth_payment
from Projects.decorators import auth_project
from datetime import date, datetime
from Pipeline.constants import StageConstant
from query_counter.decorators import queries_counter


class ProposalHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        proposals=Proposal.objects.select_related('lead').filter(lead__contact__user__id=user_dict['id'])
        proposal_data=ProposalSerializer(proposals, many=True).data
        return Response({'data': proposal_data},
                        status=status.HTTP_200_OK)


class InvoiceHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        invoices=Invoice.objects.select_related('lead').filter(lead__contact__user__id=user_dict['id'])
        invoice_data=InvoiceSerializer(invoices, many=True).data
        return Response({'data': invoice_data},
                        status=status.HTTP_200_OK)

class PaymentHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        payments=Payment.objects.select_related('lead').filter(lead__contact__user__id=user_dict['id'])
        payment_data=PaymentSerializer(payments, many=True).data
        return Response({'data': payment_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_project
    def post(self,request,user_dict,project):
        payload=request.data
        amt_received=payload.get('amount_received',None)
        _date=payload.get("date",None)
        if amt_received:
            try:
                amt_received=int(amt_received)
                if amt_received<=0:
                    return Response({'Error': "Invalid amount provided"},
                                status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid amount provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if _date:
            try:
                _date=datetime.strptime(_date, "%Y-%m-%d").date()
                if _date<project.lead.closing_date:
                    return Response({'Error': "Payment date cannot be before Lead closing date"},
                                    status=status.HTTP_400_BAD_REQUEST)
            
            except:
                return Response({'Error': "Enter Valid Date"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        payment_serializer=PaymentSerializer(data=payload)
        if payment_serializer.is_valid():
            payment=payment_serializer.save()
            payment_json=payment_serializer.data
            return Response({'data': payment_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(payment_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_payment
    def put(self,request,user_dict,payment):
        payload=request.data
        new_amt_received=payload.get('amount_received', None)
        _date=payload.get("date",None)
        if new_amt_received:
            try:
                new_amt_received=int(new_amt_received)
                if new_amt_received<=0:
                    return Response({'Error': "Invalid amount provided"},
                                status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid amount provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if _date:
            try:
                _date=datetime.strptime(_date, "%Y-%m-%d").date()
                if _date<payment.project.lead.closing_date:
                    return Response({'Error': "Payment date cannot be before Lead closing date"},
                                    status=status.HTTP_400_BAD_REQUEST)
            
            except:
                return Response({'Error': "Enter Valid Date"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        payment_serializer=PaymentSerializer(payment,data=payload,partial=True)
        if payment_serializer.is_valid():
            payment=payment_serializer.save()
            payment_json=payment_serializer.data
            return Response({'data': payment_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(payment_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)   
    
    @auth_user
    @auth_payment
    def delete(self,request,user_dict,payment):
        payment.delete()
        return Response({'Message': 'Payment Deleted Successfully'},
                        status=status.HTTP_200_OK)
             