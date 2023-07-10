from django.urls import path
from . import views


urlpatterns=[
    path('login', views.Login.as_view(), name = "Login-api"),
    path('signup', views.Signup.as_view(), name = "Signup-api"),
    path('logout', views.Logout.as_view(), name='Logout-api'),
    path('login/google/',views.GoogleLogin.as_view(), name='Google-Login-api'),
    path('signup/google/',views.GoogleSignup.as_view(), name='Google-Signup-api')
]