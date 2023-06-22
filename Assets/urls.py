from django.urls import path
from . import views


urlpatterns=[
    path('asset', views.AssetHandler.as_view(), name = "Assets-api"),
]