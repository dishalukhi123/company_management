from django.urls import path 
from .views import  CompanyView , CompanyDetailView , CompanyDepartmentView , CompanyEmployeeView

urlpatterns = [
    path('', CompanyView.as_view(), name='Company'),
    path('<int:id>/', CompanyDetailView.as_view(), name='company-detail'),
    path('<int:company_id>/departments/', CompanyDepartmentView.as_view(), name='company_departments'),
    path('<int:company_id>/employees/', CompanyEmployeeView.as_view(), name='company_employees'),
]