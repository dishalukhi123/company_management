from django.urls import path ,include
from rest_framework import routers
from . import views
from .views import  CompanyView , CompanyDetailView

urlpatterns = [
    path('company/', CompanyView.as_view(), name='Company'),
    path('company/<int:id>/', CompanyDetailView.as_view(), name='company-detail'),
]