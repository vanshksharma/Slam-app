from django.urls import path
from . import views


urlpatterns=[
    path('customer', views.CustomerHandler.as_view(), name = "Customer-api"),
    path('address', views.AddressHandler.as_view(), name = "Address-api"), 
    path('lead', views.LeadHandler.as_view(), name = "Lead-api")
]