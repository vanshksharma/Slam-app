from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Address, Lead
from .serializers import CustomerSerializer, AddressSerializer, LeadSerializer
from Auth.decorators import auth_user
from datetime import date, datetime
from .decorators import auth_customer, auth_address, auth_lead
from .constants import StageConstant
from Accounting.models import Proposal, Invoice
from Projects.models import Project
from django.db.models import Q


class CustomerHandler(APIView):
    @auth_user
    def get(self, request, user_dict):
        customers = Customer.objects.select_related(
            'user').filter(user__id=user_dict['id'])
        customer_data = CustomerSerializer(customers, many=True).data
        return Response({'data': customer_data},
                        status=status.HTTP_200_OK)

    @auth_user
    def post(self, request, user_dict):
        payload = request.data
        payload['user'] = user_dict['id']
        payload['created_at'] = date.today().isoformat()
        payload['updated_at'] = date.today().isoformat()
        customer_serializer = CustomerSerializer(data=payload)
        if customer_serializer.is_valid():
            customer = customer_serializer.save()
            customer_json = customer_serializer.data
            return Response({'data': customer_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(customer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @auth_user
    @auth_customer
    def put(self, request, user_dict, customer):
        payload = request.data
        if 'created_at' in payload:
            del payload['created_at']
        payload['updated_at'] = date.today().isoformat()
        customer_serializer = CustomerSerializer(
            customer, data=payload, partial=True)
        if customer_serializer.is_valid():
            updated_customer = customer_serializer.save()
            updated_customer_json = customer_serializer.data
            return Response({'data': updated_customer_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(customer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @auth_user
    @auth_customer
    def delete(self, request, user_dict, customer):
        customer.delete()
        return Response({'Message': 'Customer Deleted Successfully'},
                        status=status.HTTP_200_OK)


class AddressHandler(APIView):
    @auth_user
    @auth_customer
    def get(self, request, user_dict, customer):
        address = Address.objects.select_related(
            'customer').filter(customer__id=customer.id)
        address_data = AddressSerializer(address, many=True).data
        return Response({'data': address_data},
                        status=status.HTTP_200_OK)

    @auth_user
    @auth_customer
    def post(self, request, user_dict, customer):
        payload = request.data
        payload['created_at'] = date.today().isoformat()
        payload['updated_at'] = date.today().isoformat()
        adddress_serializer = AddressSerializer(data=payload)
        if adddress_serializer.is_valid():
            address = adddress_serializer.save()
            address_json = adddress_serializer.data
            return Response({'data': address_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(adddress_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @auth_user
    @auth_address
    def put(self, request, user_dict, address):
        payload = request.data
        if 'created_at' in payload:
            del payload['created_at']
        payload['updated_at'] = date.today().isoformat()
        address_serializer = AddressSerializer(
            address, data=payload, partial=True)
        if address_serializer.is_valid():
            updated_address = address_serializer.save()
            updated_address_json = address_serializer.data
            return Response({'data': updated_address_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(address_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @auth_user
    @auth_address
    def delete(self, request, user_dict, address):
        address.delete()
        return Response({'Message': 'Address Deleted Successfully'},
                        status=status.HTTP_200_OK)


class LeadHandler(APIView):
    @auth_user
    def get(self, request, user_dict):
        leads = Lead.objects.select_related('customer').filter(
            customer__user__id=user_dict['id'])
        lead_data = LeadSerializer(leads, many=True).data
        return Response({'data': lead_data},
                        status=status.HTTP_200_OK)

    @auth_user
    @auth_customer
    def post(self, request, user_dict, customer):
        payload = request.data
        payload['created_at']=date.today()
        payload['updated_at'] = date.today()
        stage = payload.get('stage', None)
        closing_date = payload.get('closing_date', None)
        confidence = payload.get('confidence', None)
        amount=payload.get('amount',None)

        # Stage Check
        if stage:
            try:
                stage = StageConstant[stage.upper()]
                payload['stage'] = stage.name
                
                if stage==StageConstant.OPPORTUNITY:
                    if amount:
                        return Response({'Error': "Amount cannot be provided for a Lead in Opportunity stage"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    if closing_date:
                            return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided a closing date."},
                                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    if stage == StageConstant.CONTACTED or stage == StageConstant.NEGOTIATION:
                        if closing_date:
                            return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided a closing date."},
                                            status=status.HTTP_400_BAD_REQUEST)
                        if not amount:
                            return Response({'Error': "Amount cannot be null for Contacted or Negotiation leads"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        
                    else:
                        if stage==StageConstant.CLOSED_WON:
                            if not amount:
                                return Response({'Error': "Amount cannot be null for Closed Won leads"},
                                                status=status.HTTP_400_BAD_REQUEST)
                            if not closing_date:
                                payload['closing_date'] = date.today().isoformat()
                            else:
                                try:
                                    closing_date_temp = datetime.strptime(closing_date, "%Y-%m-%d").date()
                                    payload['closing_date']=closing_date
                                    if closing_date_temp < payload['created_at']:
                                        return Response({'Error': "Closing date cannot be before the date of Lead creation"},
                                                        status=status.HTTP_400_BAD_REQUEST)
                                except:
                                    return Response({'Error': "Enter Valid Closing Date"},
                                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': 'Invalid Stage Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if closing_date:
            if not stage:
                return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided a closing date"},
                                    status=status.HTTP_400_BAD_REQUEST)

        if amount:
            if not stage:
                return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided an Amount"},
                                    status=status.HTTP_400_BAD_REQUEST)
        # Confidence check
        if confidence:
            try:
                confidence = float(confidence)
                if confidence >= 0.0 and confidence <= 1.0:
                    payload['confidence'] = confidence
                else:
                    return Response({'Error': 'Confidence must be between 0 and 1'},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': 'Invalid Confidence Level Provided'},
                                status=status.HTTP_400_BAD_REQUEST)

        lead_serializer = LeadSerializer(data=payload)
        if lead_serializer.is_valid():
            lead = lead_serializer.save()
            
            if lead.stage == StageConstant.CONTACTED.name or lead.stage == StageConstant.NEGOTIATION.name:
                # Creating Proposal
                proposal=Proposal.objects.create(lead=lead,amount=lead.amount,date=lead.created_at)
                proposal.save()

            lead_json = lead_serializer.data
            return Response({'data': lead_json},
                            status=status.HTTP_200_OK)

        else:
            return Response(lead_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @auth_user
    @auth_lead
    def put(self, request, user_dict, lead):
        payload = request.data
        stage = payload.get('stage', None)
        closing_date = payload.get('closing_date', None)
        confidence = payload.get('confidence', None)
        amount=payload.get('amount',None)

        if stage:
            try:
                stage = StageConstant[stage.upper()]
                payload['stage'] = stage.name
                
                if not stage==StageConstant.CLOSED_WON:
                    projects=Project.objects.select_related('lead').filter(lead__id=lead.id).count()
                    if projects>0:
                        return Response({'Error': f"Cannot mark the Lead as {stage.name.capitalize()} as it contains Projects"},
                                        status=status.HTTP_400_BAD_REQUEST)
                
                if stage==StageConstant.OPPORTUNITY:
                    if amount:
                        return Response({'Error': "Amount cannot be provided for a Lead in Opportunity stage"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    if closing_date:
                            return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided a closing date."},
                                            status=status.HTTP_400_BAD_REQUEST)
                    payload['amount']=None
                    payload['closing_date']=None

                else:
                    if stage == StageConstant.CONTACTED or stage == StageConstant.NEGOTIATION:
                        if closing_date:
                            return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided a closing date"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        if lead.closing_date:
                            payload['closing_date'] = None
                        
                        if not amount:
                            if not lead.amount:
                                return Response({'Error': "Amount cannot be null for Contacted or Negotiation leads"},
                                                status=status.HTTP_400_BAD_REQUEST)

                    else:
                        if stage==StageConstant.CLOSED_WON:
                            if not amount:
                                if not lead.amount:
                                    return Response({'Error': "Amount cannot be null for Closed Won leads"},
                                                    status=status.HTTP_400_BAD_REQUEST)
                            if closing_date:
                                try:
                                    closing_date_temp = datetime.strptime(
                                        closing_date, "%Y-%m-%d").date()
                                    if closing_date_temp < lead.created_at:
                                        return Response({'Error': "Closing date can be before the date of Lead creation"},
                                                        status=status.HTTP_400_BAD_REQUEST)
                                except:
                                    return Response({'Error': "Enter Valid Closing Date"},
                                                    status=status.HTTP_400_BAD_REQUEST)
                            else:
                                payload['closing_date'] = date.today().isoformat()
                        
            except:
                return Response({'Error': 'Invalid Stage Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if closing_date:
            if not stage:
                if not (lead.stage==StageConstant.CLOSED_WON.name or lead.stage==StageConstant.CLOSED_LOST.name):
                    return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided a closing date"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    try:
                        closing_date_temp = datetime.strptime(closing_date, "%Y-%m-%d").date()
                        if closing_date_temp < lead.created_at:
                            return Response({'Error': "Closing date can be before the date of Lead creation"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        projects_before_new_closing_date=Project.objects.select_related('lead').filter(Q(lead__id=lead.id) & Q(start_date__lt=closing_date)).count()
                        if projects_before_new_closing_date>0:
                            return Response({'Error': "Lead contains Projects with start date before the closing date of Lead"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    except:
                        return Response({'Error': "Enter Valid Closing Date"},
                                        status=status.HTTP_400_BAD_REQUEST)
        
        if amount:
            if not stage:
                if lead.stage==StageConstant.OPPORTUNITY.name:
                    return Response({'Error': "Amount cannot be provided for a Lead in Opportunity stage"},
                                    status=status.HTTP_400_BAD_REQUEST)

        # Confidence Check
        if confidence:
            try:
                confidence = float(confidence)
                if confidence >= 0.0 and confidence <= 1.0:
                    payload['confidence'] = confidence
                else:
                    return Response({'Error': 'Confidence must be between 0 and 1'},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': 'Invalid Confidence Level Provided'},
                                status=status.HTTP_400_BAD_REQUEST)

        payload['updated_at']=date.today().isoformat()
        lead_serializer = LeadSerializer(lead, data=payload, partial=True)
        if lead_serializer.is_valid():
            lead = lead_serializer.save()
            if lead.stage == StageConstant.CONTACTED.name or lead.stage == StageConstant.NEGOTIATION.name:
                try:
                    proposal=Proposal.objects.select_related('lead').get(lead__id=lead.id)
                    proposal.amount=lead.amount
                    proposal.date=lead.updated_at
                except Proposal.DoesNotExist:
                    proposal=Proposal.objects.create(lead=lead,amount=lead.amount,date=lead.updated_at)
                finally:
                    proposal.save()
            
            elif lead.stage==StageConstant.CLOSED_WON.name or lead.stage==StageConstant.CLOSED_LOST.name or lead.stage==StageConstant.OPPORTUNITY.name:
                #Delete Proposal for that lead if exists
                try:
                    proposal=Proposal.objects.select_related('lead').get(lead__id=lead.id)
                    proposal.delete()
                except Proposal.DoesNotExist:
                    pass
                    
            lead_json = lead_serializer.data
            return Response({'data': lead_json},
                            status=status.HTTP_200_OK)

        else:
            return Response(lead_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @auth_user
    @auth_lead
    def delete(self, request, user_dict, lead):
        lead.delete()
        return Response({'Message': 'Lead Deleted Successfully'},
                        status=status.HTTP_200_OK)
