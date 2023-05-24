from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proposal, Payment, Invoice
from .serializers import ProposalSerializer, PaymentSerializer, InvoiceSerializer
from Auth.decorators import auth_user
from Pipeline.decorators import auth_lead
from .decorators import auth_proposal, auth_invoice, auth_payment
from Projects.decorators import auth_project
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


class InvoiceHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        invoices=Invoice.objects.select_related('lead').filter(lead__customer__user__id=user_dict['id'])
        invoice_data=InvoiceSerializer(invoices, many=True).data
        return Response({'data': invoice_data},
                        status=status.HTTP_200_OK)

class PaymentHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        payments=Payment.objects.select_related('project').filter(project__lead__customer__user__id=user_dict['id'])
        payment_data=PaymentSerializer(payments, many=True).data
        return Response({'data': payment_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_project
    def post(self,request,user_dict,project):
        payload=request.data
        amt_received=payload.get('amount_received',None)
        if amt_received:
            try:
                amt_received=int(amt_received)
                if amt_received>project.value:
                    return Response({'Error': "Amount Received cannot be greater than the value of the project"},
                                    status=status.HTTP_400_BAD_REQUEST)
                
                if amt_received+project.amount_paid>project.value:
                    return Response({'Error': "Amount already paid exceeds the project value"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid amount provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        payment_serializer=PaymentSerializer(data=payload)
        if payment_serializer.is_valid():
            payment=payment_serializer.save()
            #Increasing the project amount_paid value
            project.amount_paid+=amt_received
            project.save()
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
        if new_amt_received:
            try:
                new_amt_received=int(new_amt_received)
                project=payment.project
                existing_amt=payment.project.amount_paid
                payment_amount=payment.amount_received
                if existing_amt-payment_amount+new_amt_received>project.value:
                    return Response({'Error': "Amount already paid exceeds the project value"},
                                status=status.HTTP_400_BAD_REQUEST)
                
                project.amount_paid+=(new_amt_received-payment_amount)
                project.save()
            except:
                return Response({'Error': "Invalid amount provided"},
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
        project=payment.project
        project.amount_paid-=payment.amount_received
        project.save()
        
        payment.delete()
        return Response({'Message': 'Payment Deleted Successfully'},
                        status=status.HTTP_200_OK)
             