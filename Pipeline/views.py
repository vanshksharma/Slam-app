from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact, Address, Lead
from .serializers import ContactSerializer, AddressSerializer, LeadSerializer
from Auth.decorators import auth_user
from datetime import date, datetime
from .decorators import auth_contact, auth_address, auth_lead
from .constants import StageConstant
from Pipeline.constants import TypeConstant
from django.db.models import Q


class ContactHandler(APIView):
    @auth_user
    def get(self, request, user_dict):
        contacts = Contact.objects.select_related(
            'user').filter(user__id=user_dict['id'])
        contact_data = ContactSerializer(contacts, many=True).data
        return Response({'data': contact_data},
                        status=status.HTTP_200_OK)

    @auth_user
    def post(self, request, user_dict):
        payload = request.data
        contact_type=payload.get('contact_type',None)
        payload['user'] = user_dict['id']
        email=payload.get('email',None)
        payload['created_at'] = date.today().isoformat()
        payload['updated_at'] = date.today().isoformat()
        if contact_type:
            try:
                contact_type=TypeConstant[contact_type.upper()]
                payload['contact_type']=contact_type.name
            except:
                return Response({'Error': 'Invalid Contact Type Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
            
        if email:
            contacts_with_same_email_for_the_user=Contact.objects.select_related('user').filter(Q(email=email) & Q(user__id=user_dict['id'])).count()
            if contacts_with_same_email_for_the_user>0:
                return Response({'Error': 'Contact with this email already exists'},
                                status=status.HTTP_400_BAD_REQUEST)
                    
        contact_serializer = ContactSerializer(data=payload)
        if contact_serializer.is_valid():
            contact = contact_serializer.save()
            contact_json = contact_serializer.data
            return Response({'data': contact_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(contact_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @auth_user
    @auth_contact
    def put(self, request, user_dict, contact):
        payload = request.data
        if 'created_at' in payload:
            del payload['created_at']
        payload['updated_at'] = date.today().isoformat()
        email=payload.get('email',None)
        contact_type=payload.get('contact_type',None)
        if contact_type:
            try:
                contact_type=TypeConstant[contact_type.upper()]
                payload['contact_type']=contact_type.name
            except:
                return Response({'Error': 'Invalid Contact Type Provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        if email:
            contacts_with_same_email_for_the_user=Contact.objects.select_related('user').filter(Q(email=email) & Q(user__id=user_dict['id'])).count()
            if contacts_with_same_email_for_the_user>0:
                return Response({'Error': 'Contact with this email already exists'},
                                status=status.HTTP_400_BAD_REQUEST)
        contact_serializer = ContactSerializer(
            contact, data=payload, partial=True)
        if contact_serializer.is_valid():
            updated_contact = contact_serializer.save()
            updated_contact_json = contact_serializer.data
            return Response({'data': updated_contact_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(contact_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @auth_user
    @auth_contact
    def delete(self, request, user_dict, contact):
        contact.delete()
        return Response({'Message': 'Contact Deleted Successfully'},
                        status=status.HTTP_200_OK)


class AddressHandler(APIView):
    @auth_user
    def get(self, request, user_dict):
        address = Address.objects.select_related(
            'contact').filter(contact__user__id=user_dict['id'])
        address_data = AddressSerializer(address, many=True).data
        return Response({'data': address_data},
                        status=status.HTTP_200_OK)

    @auth_user
    @auth_contact
    def post(self, request, user_dict, contact):
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
        leads = Lead.objects.select_related('contact').filter(
            contact__user__id=user_dict['id'])
        lead_data = LeadSerializer(leads, many=True).data
        return Response({'data': lead_data},
                        status=status.HTTP_200_OK)

    @auth_user
    @auth_contact
    def post(self, request, user_dict, contact):
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
                            return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided a closing date"},
                                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    if stage == StageConstant.CONTACTED or stage == StageConstant.NEGOTIATION:
                        if closing_date:
                            return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided a closing date"},
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
                return Response({'Error': "Amount cannot be provided for a Lead in Opportunity stage"},
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
        payload['updated_at']=date.today().isoformat()
        if 'created_at' in payload:
            del payload['created_at']

        if stage:
            try:
                stage = StageConstant[stage.upper()]
                payload['stage'] = stage.name
                
                if stage==StageConstant.OPPORTUNITY:
                    if amount:
                        return Response({'Error': "Amount cannot be provided for a Lead in Opportunity stage"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    if closing_date:
                            return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided a closing date"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    payload['amount']=None
                    payload['closing_date']=None

                else:
                    if stage == StageConstant.CONTACTED or stage == StageConstant.NEGOTIATION:
                        if closing_date:
                            return Response({'Error': "Only leads in Closed Won or Closed Lost stage can be provided a closing date"},
                                            status=status.HTTP_400_BAD_REQUEST)
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

        lead_serializer = LeadSerializer(lead, data=payload, partial=True)
        if lead_serializer.is_valid():
            lead = lead_serializer.save()
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
