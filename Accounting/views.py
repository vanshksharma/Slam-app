from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proposal, Payment, Invoice, Item
from .serializers import ProposalSerializer, PaymentSerializer, InvoiceSerializer, ItemSerializer
from Auth.decorators import auth_user
from Pipeline.decorators import auth_contact
from .decorators import auth_payment, auth_proposal, auth_invoice
from Projects.models import Project
from Pipeline.models import Lead
from django.db.models import Q
from datetime import datetime,date
from django.shortcuts import get_object_or_404
from django.http import Http404

class ProposalHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        proposals=Proposal.objects.select_related('contact').filter(contact__user__id=user_dict['id'])
        items=Item.objects.select_related('proposal').filter(proposal__contact__user__id=user_dict['id'])
        proposal_data=ProposalSerializer(proposals, many=True).data
        items_data=ItemSerializer(items, many=True).data
        return Response({'data': {'proposals': proposal_data, 'items': items_data}},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_contact
    def post(self,request,user_dict,contact):
        payload=request.data
        lead=payload.get('lead', None)
        proposal_number=payload.get('proposal_number', None)
        creation_date=payload.get('creation_date', None)
        expiry_date=payload.get('expiry_date', None)
        tax=payload.get('tax', None)
        amount=payload.get('amount', None)
        items=payload.pop('items', None)
        if lead:
            try:
                lead=Lead.objects.select_related('contact').get(id=lead)
                if lead.contact.user.id != user_dict['id']:
                    return Response({'Error': "The Lead does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Lead.DoesNotExist,ValueError):
                return Response({'Error': "Please Enter Valid Lead ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if proposal_number:
            proposals_with_same_proposal_number=Proposal.objects.select_related('contact').filter(Q(contact__user__id=user_dict['id']) & Q(proposal_number=proposal_number)).count()
            if proposals_with_same_proposal_number > 0:
                return Response({'Error': "Proposal Number Already Exists"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if expiry_date:
            try:
                expiry_date_temp=datetime.strptime(expiry_date, '%Y-%m-%d').date()
                if creation_date:
                    try:
                        creation_date_temp=datetime.strptime(creation_date, '%Y-%m-%d').date()
                    except:
                        return Response({'Error': "Please Enter Valid Creation Date"},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    creation_date_temp=date.today()
                
                if expiry_date_temp < creation_date_temp:
                    return Response({'Error': "Expiry Date Cannot be before Creation Date"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Please Enter Valid Expiry Date"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if tax:
            try:
                tax_temp=float(tax)
                if tax_temp < 0:
                    return Response({'Error': "Please Enter Valid Tax"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Please Enter Valid Tax"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if amount:
            try:
                amount_temp=float(amount)
                if amount_temp < 0:
                    return Response({'Error': "Please Enter Valid Amount"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Please Enter Valid Amount"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        proposal_serializer=ProposalSerializer(data=payload)
        if proposal_serializer.is_valid():
            proposal=proposal_serializer.save()
            proposal_json=proposal_serializer.data
            # Logic for creating items
            proposal_id=proposal.id
            items_json=[]
            if items:
                for item in items:
                    item.pop('id',None)
                    item['proposal']=proposal_id
                    item_serializer=ItemSerializer(data=item)
                    if item_serializer.is_valid():
                        item_serializer.save()
                        items_json.append(item_serializer.data)
                    else:
                        proposal.delete()
                        return Response(item_serializer.errors,
                                        status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'data': {'proposal': proposal_json, 'items': items_json}},
                        status=status.HTTP_200_OK)
        else:
            return Response(proposal_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_proposal
    def put(self,request,user_dict,proposal):
        payload=request.data
        lead=payload.get('lead', None)
        proposal_number=payload.get('proposal_number', None)
        creation_date=payload.get('creation_date', None)
        expiry_date=payload.get('expiry_date', None)
        tax=payload.get('tax', None)
        amount=payload.get('amount', None)
        items=payload.pop('items', None)
        payload.pop('id',None)
        if lead:
            try:
                lead=Lead.objects.select_related('contact').get(id=lead)
                if lead.contact.user.id != user_dict['id']:
                    return Response({'Error': "The Lead does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Lead.DoesNotExist,ValueError):
                return Response({'Error': "Please Enter Valid Lead ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if proposal_number:
            proposals_with_same_proposal_number=Proposal.objects.select_related('contact').filter(Q(contact__user__id=user_dict['id']) & Q(proposal_number=proposal_number) & ~Q(id=proposal.id)).count()
            if proposals_with_same_proposal_number > 0:
                return Response({'Error': "Proposal Number Already Exists"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if creation_date and not expiry_date:
            try:
                creation_date_temp=datetime.strptime(creation_date, "%Y-%m-%d").date()
                if creation_date_temp>proposal.expiry_date:
                    return Response({'Error': "Proposal Creation Date cannot be after Expiry Date"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Creation Date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if expiry_date and not creation_date:
            try:
                expiry_date_temp=datetime.strptime(expiry_date, "%Y-%m-%d").date()
                if expiry_date_temp<proposal.creation_date:
                    return Response({'Error': "Proposal Expiry Date cannot be before Creation Date"},
                                        status=status.HTTP_400_BAD_REQUEST)
            
            except:
                return Response({'Error': "Invalid Expiry Date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if creation_date and expiry_date:
            try:
                creation_date_temp=datetime.strptime(creation_date, "%Y-%m-%d").date()
                expiry_date_temp=datetime.strptime(expiry_date, "%Y-%m-%d").date()
                if expiry_date_temp<creation_date_temp:
                        return Response({'Error': "Expiry Date cannot be before Creation Date"},
                                        status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Invalid Creation Date or Expiry Date provided"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if tax:
            try:
                tax_temp=float(tax)
                if tax_temp < 0:
                    return Response({'Error': "Please Enter Valid Tax"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Please Enter Valid Tax"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if amount:
            try:
                amount_temp=float(amount)
                if amount_temp < 0:
                    return Response({'Error': "Please Enter Valid Amount"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': "Please Enter Valid Amount"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        # Getting all the items for this proposal
        items_queryset=Item.objects.select_related('proposal').filter(proposal__id=proposal.id)
        proposal_serializer=ProposalSerializer(proposal,data=payload,partial=True)
        if proposal_serializer.is_valid():
            # Saving at last because we cannot delete the proposal if the items are not valid
            # Validating items
            not_saved_items=[]
            items_json=[]
            proposal_id=proposal.id
            if items:
                for item in items:
                    item.pop('id',None)
                    if item.get('item',None):
                        try:
                            item_instance=get_object_or_404(items_queryset,id=item['item'])
                            item_serializer=ItemSerializer(item_instance,data=item,partial=True)
                            if item_serializer.is_valid():
                                not_saved_items.append(item_serializer)
                            else:
                                return Response(item_serializer.errors,
                                                status=status.HTTP_400_BAD_REQUEST)
                        except Http404:
                            return Response({'Error': "Invalid Item ID provided"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        item['proposal']=proposal_id
                        item_serializer=ItemSerializer(data=item)
                        if item_serializer.is_valid():
                            not_saved_items.append(item_serializer)
                        else:
                            return Response(item_serializer.errors,
                                            status=status.HTTP_400_BAD_REQUEST)
            
                      
                # Everything is valid, so saving the items
                _=list(map(lambda x: x.save(), not_saved_items))
                items_json=list(map(lambda x: x.data, not_saved_items)) # Saved the items, now getting the data using the serializer
            
            proposal=proposal_serializer.save()
            proposal_json=proposal_serializer.data
            return Response({'data': {'proposal': proposal_json, 'items': items_json}},
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
        payments=Payment.objects.select_related('contact').filter(contact__user__id=user_dict['id'])
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
             