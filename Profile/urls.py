from django.urls import path
from . import views


urlpatterns=[
    path('profile', views.ProfileHandler.as_view(), name = "Profile-api")
]