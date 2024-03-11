from django.urls import path 
from .views import  EmployeeView , EmployeeDetailView

urlpatterns = [
    path('', EmployeeView.as_view(), name='department'),
    path('<int:id>/', EmployeeDetailView.as_view(), name='company-detail'),

]