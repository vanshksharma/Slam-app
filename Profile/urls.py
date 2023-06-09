from django.urls import path
from . import views


urlpatterns=[
    path('profile', views.ProfileHandler.as_view(), name = "Profile-api"),
    path('account', views.AccountHandler.as_view(), name = "Account-api"),
    path('integration/calender', views.CalenderIntegrationHandler.as_view(), name = "Calender-Integration-api"),
    path('integration/zoom', views.ZoomIntegrationHandler.as_view(), name = "Zoom-Integration-api"),
    path('integration', views.IntegrationHandler.as_view(), name = "Integration-api")
]