from django.urls import path
from . import views


urlpatterns=[
    path('login', views.Login.as_view(), name = "Login-api"),
    path('signup', views.Signup.as_view(), name = "Signup-api")
]