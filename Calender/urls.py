from django.urls import path
from . import views


urlpatterns=[
    path('event', views.EventHandler.as_view(), name = "Event-api")
]