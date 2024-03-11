from django.urls import path 
from .views import  DepartmentView , DepartmentDetailView , DepartmentEmployee
 
urlpatterns = [
    path('', DepartmentView.as_view(), name='department'),
    path('<int:id>/', DepartmentDetailView.as_view(), name='company-detail'),
    path('<int:department_id>/employees/', DepartmentEmployee.as_view(), name='department_employees'),
]