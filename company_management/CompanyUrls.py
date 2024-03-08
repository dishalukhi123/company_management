from django.urls import path 
from .views import  CompanyView , CompanyDetailView

urlpatterns = [
    path('', CompanyView.as_view(), name='Company'),
    path('<int:id>/', CompanyDetailView.as_view(), name='company-detail'),
]