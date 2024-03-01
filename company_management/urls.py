from django.urls import path ,include
from rest_framework import routers
from . import views
from .views import  UserRegistrationView , UserLoginView , UserProfileView , UserListView , UserDetailView , UserUpdateView , UserDeleteView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:id>/edit/', UserUpdateView.as_view(), name='user-edit'),
    path('users/<int:id>/delete/', UserDeleteView.as_view(), name='user-delete'),

 ]