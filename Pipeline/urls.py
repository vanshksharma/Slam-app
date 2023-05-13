from django.urls import path
from . import views


urlpatterns=[
    path('customer', views.CustomerHandler.as_view(), name = "Customer-api"), 
]