from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from company_management.serializers import UserRegistrationSerializer , UserLoginSerializer , UserProfileSerializer , UserListSerializer , UserDetailSerializer , CompanySerializer , CompanyDetailSerializer
from django.contrib.auth import authenticate 
from company_management.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User , Company
from django.http import Http404
from django.shortcuts import get_object_or_404


def get_tokens_for_user(user):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    return {
        'refresh': str(refresh_token),
        'access': str(access_token),
    }


class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
          user = serializer.save()
          token = get_tokens_for_user(user)
          return Response({'status': status.HTTP_201_CREATED,'success': True, 'message':'Registration Successful', 'data': {'token': token}}, status=status.HTTP_201_CREATED)
    return Response({'status': status.HTTP_201_CREATED,'success': True, 'message':'Registration Successful', 'data': {'token': token}}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token = get_tokens_for_user(user)  
        return Response({'status': status.HTTP_200_OK, 'success': True, 'token': token}, status=status.HTTP_200_OK)

    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated] 

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'User Profile', 'data': serializer.data})
    

class UserListView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, format=None):
        queryset = User.objects.filter(is_active=True)
        serializer = UserListSerializer(queryset, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'User List', 'data': serializer.data})
    

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            user = get_object_or_404(User, id=id)
            serializer = UserProfileSerializer(user)
            return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'User Detail', 'data': serializer.data})
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'message': 'User not found'})

    def patch(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            serializer = UserDetailSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 200, 'success': True, 'message': 'User details updated successfully'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'message': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, format=None):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, 'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class CompanyView(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'data': serializer.data})

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': status.HTTP_200_OK, 'success': True, 'data': serializer.data})
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': True , 'data': serializer.errors})  


class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            company = get_object_or_404(Company, id=id)
            serializer = CompanyDetailSerializer(company)
            return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Company Detail', 'data': serializer.data})
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'message': 'Company not found'})


    def patch(self, request, id):
        try:
            company = get_object_or_404(Company, id=id)
            serializer = CompanyDetailSerializer(company, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Company details updated successfully'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'message': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, format=None):
        try:
            company = get_object_or_404(Company, id=id)
            company.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, 'message': 'Company deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'message': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)