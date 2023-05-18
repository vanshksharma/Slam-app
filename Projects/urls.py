from django.urls import path
from . import views


urlpatterns=[
    path('project', views.ProjectHandler.as_view(), name = "Project-api")
]