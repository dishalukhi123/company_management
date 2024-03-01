from django.urls import path ,include
from rest_framework import routers
from . import views
from .views import  UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
 ]