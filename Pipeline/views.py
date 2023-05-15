from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,Address
from .serializers import CustomerSerializer,AddressSerializer
from Auth.decorators import auth_user
from datetime import date
from .decorators import auth_customer,auth_address


class CustomerHandler(APIView):
    @auth_user
    def get(self,request,user_dict):
        customers=Customer.objects.select_related('user').filter(user__id=user_dict['id'])
        customer_data=CustomerSerializer(customers,many=True).data
        return Response({'data': customer_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    def post(self,request,user_dict):
        payload=request.data
        payload['user']=user_dict['id']
        customer_serializer=CustomerSerializer(data=payload)
        if customer_serializer.is_valid():
            customer=customer_serializer.save()
            customer_json=customer_serializer.data
            return Response({'data': customer_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(customer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
            
    @auth_user
    @auth_customer
    def put(self,request,user_dict,customer):
        payload=request.data
        payload['updated_at']=date.today().isoformat()
        customer_serializer=CustomerSerializer(customer,data=payload,partial=True)
        if customer_serializer.is_valid():
            updated_customer=customer_serializer.save()
            updated_customer_json=customer_serializer.data
            return Response({'data':updated_customer_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(customer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_customer
    def delete(self,request,user_dict,customer):
        customer.delete()
        return Response({'Message': 'Customer Deleted Successfully'},
                        status=status.HTTP_200_OK)    
        
        
class AddressHandler(APIView):
    @auth_user
    @auth_customer
    def get(self,request,user_dict,customer):
        address=Address.objects.select_related('customer').filter(customer__id=customer.id)
        address_data=AddressSerializer(address,many=True).data
        return Response({'data':address_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    @auth_customer
    def post(self,request,user_dict,customer):
        payload=request.data
        adddress_serializer=AddressSerializer(data=payload)
        if adddress_serializer.is_valid():
            address=adddress_serializer.save()
            address_json=adddress_serializer.data
            return Response({'data':address_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(adddress_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_address
    def put(self,request,user_dict,address):
        payload=request.data
        payload['updated_at']=date.today().isoformat()
        address_serializer=AddressSerializer(address,data=payload,partial=True)
        if address_serializer.is_valid():
            updated_address=address_serializer.save()
            updated_address_json=address_serializer.data
            return Response({'data':updated_address_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(address_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_address
    def delete(self,request,user_dict,address):
        address.delete()
        return Response({'Message': 'Address Deleted Successfully'},
                        status=status.HTTP_200_OK)
            
        