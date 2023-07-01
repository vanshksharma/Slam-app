from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact, Lead
from .serializers import ContactSerializer, LeadSerializer
from Auth.decorators import auth_user
from datetime import date, datetime
from .decorators import auth_contact, auth_lead
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
        payload.pop('created_at', None)
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

        # Stage Check
        if stage:
            try:
                stage = StageConstant[stage.upper()]
                payload['stage'] = stage.name
                if stage==StageConstant.CLOSED_WON:
                    if not closing_date:
                        payload['closing_date'] = date.today().isoformat()
                    else:
                        try:
                            closing_date_temp = datetime.strptime(closing_date, "%Y-%m-%d").date()
                        except:
                            return Response({'Error': "Enter Valid Closing Date"},
                                            status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error': 'Invalid Stage Provided'},
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
        payload['updated_at']=date.today().isoformat()
        payload.pop('created_at',None)

        if stage:
            try:
                stage = StageConstant[stage.upper()]
                payload['stage'] = stage.name
                
                if stage==StageConstant.CLOSED_WON:
                    if closing_date:
                        try:
                            closing_date_temp = datetime.strptime(closing_date, "%Y-%m-%d").date()
                        except:
                            return Response({'Error': "Enter Valid Closing Date"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        if not lead.closing_date:
                            payload['closing_date'] = date.today().isoformat()
                        
            except:
                return Response({'Error': 'Invalid Stage Provided'},
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
