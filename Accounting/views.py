from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proposal, Payment, Invoice
from .serializers import ProposalSerializer, PaymentSerializer, InvoiceSerializer
from Auth.decorators import auth_user
from Pipeline.decorators import auth_contact
from .decorators import auth_payment, auth_proposal, auth_invoice
from Projects.models import Project
from Pipeline.models import Lead


class ProposalHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        proposals=Proposal.objects.select_related('contact').filter(contact__user__id=user_dict['id'])
        proposal_data=ProposalSerializer(proposals, many=True).data
        return Response({'data': proposal_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_contact
    def post(self,request,user_dict,contact):
        payload=request.data
        lead=payload.get('lead', None)
        if lead:
            try:
                lead=Lead.objects.select_related('contact').get(id=lead)
                if lead.contact.user.id != user_dict['id']:
                    return Response({'Error': "The Lead does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Lead.DoesNotExist,ValueError):
                return Response({'Error': "Please Enter Valid Lead ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        
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
        lead=payload.get('lead', None)
        if lead:
            try:
                lead=Lead.objects.select_related('contact').get(id=lead)
                if lead.contact.user.id != user_dict['id']:
                    return Response({'Error': "The Lead does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Lead.DoesNotExist,ValueError):
                return Response({'Error': "Please Enter Valid Lead ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        
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
        invoices=Invoice.objects.select_related('contact').filter(contact__user__id=user_dict['id'])
        invoice_data=InvoiceSerializer(invoices, many=True).data
        return Response({'data': invoice_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_contact
    def post(self,request,user_dict,contact):
        payload=request.data
        project=payload.get('project', None)
        if project:
            try:
                project=Project.objects.select_related('contact').get(id=project)
                if project.contact.user.id != user_dict['id']:
                    return Response({'Error': "The Project does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Project.DoesNotExist,ValueError):
                return Response({'Error': "Please Enter Valid Project ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        
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
        project=payload.get('project', None)
        if project:
            try:
                project=Project.objects.select_related('contact').get(id=project)
                if project.contact.user.id != user_dict['id']:
                    return Response({'Error': "The Project does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Project.DoesNotExist,ValueError):
                return Response({'Error': "Please Enter Valid Project ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        
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


class PaymentHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        payments=Payment.objects.select_related('lead').filter(lead__contact__user__id=user_dict['id'])
        payment_data=PaymentSerializer(payments, many=True).data
        return Response({'data': payment_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_contact
    def post(self,request,user_dict,contact):
        payload=request.data
        project=payload.get('project', None)
        if project:
            try:
                project=Project.objects.select_related('contact').get(id=project)
                if project.contact.user.id != user_dict['id']:
                    return Response({'Error': "The Project does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Project.DoesNotExist,ValueError):
                return Response({'Error': "Please Enter Valid Project ID"},
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
        project=payload.get('project', None)
        if project:
            try:
                project=Project.objects.select_related('contact').get(id=project)
                if project.contact.user.id != user_dict['id']:
                    return Response({'Error': "The Project does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Project.DoesNotExist,ValueError):
                return Response({'Error': "Please Enter Valid Project ID"},
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
             