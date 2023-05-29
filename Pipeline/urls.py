from django.urls import path
from . import views


urlpatterns=[
    path('contact', views.ContactHandler.as_view(), name = "Contact-api"),
    path('address', views.AddressHandler.as_view(), name = "Address-api"), 
    path('lead', views.LeadHandler.as_view(), name = "Lead-api")
]