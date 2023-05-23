from django.urls import path
from . import views


urlpatterns=[
    path('proposal', views.ProposalHandler.as_view(), name = "Proposal-api"),
    path('invoice', views.InvoiceHandler.as_view(), name = "Invoice-api"),
    path('payment', views.PaymentHandler.as_view(), name='Payment-api')
]