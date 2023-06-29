from django.urls import path
from . import views


urlpatterns=[
    path('contact', views.ContactHandler.as_view(), name = "Contact-api"),
    path('lead', views.LeadHandler.as_view(), name = "Lead-api")
]