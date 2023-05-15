from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
from Auth.decorators import auth_user
from datetime import date


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
        print(payload)
        customer_serializer=CustomerSerializer(data=payload)
        if customer_serializer.is_valid():
            customer=customer_serializer.save()
            customer_json=CustomerSerializer(customer).data
            return Response({'data': customer_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(customer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
            
    @auth_user
    def put(self,request,user_dict):
        payload=request.data
        customer_id=payload['id']
        try:
            customer=Customer.objects.select_related('user').get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({'Error':"Please Enter Valid Customer ID"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if customer.user.id!=user_dict['id']:
            return Response({'Error':"The Customer does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)
        
        payload['updated_at']=date.today().isoformat()
        customer_serializer=CustomerSerializer(customer,data=payload,partial=True)
        if customer_serializer.is_valid():
            updated_customer=customer_serializer.save()
            updated_customer_json=CustomerSerializer(updated_customer).data
            return Response({'data':updated_customer_json},
                            status=status.HTTP_200_OK)
        else:
            return Response(customer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
       
        
        
        

