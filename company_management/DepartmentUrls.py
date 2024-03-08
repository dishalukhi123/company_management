from django.urls import path 
from .views import  DepartmentView , DepartmentDetailView

urlpatterns = [
    path('', DepartmentView.as_view(), name='department'),
    path('<int:id>/', DepartmentDetailView.as_view(), name='company-detail'),

]