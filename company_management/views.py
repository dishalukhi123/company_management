from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.exceptions import ValidationError
from company_management.serializers import UserRegistrationSerializer , UserLoginSerializer , UserProfileSerializer , UserListSerializer , UserDetailSerializer , CompanySerializer , CompanyDetailSerializer , DepartmentSerializer , DepartmentDetailSerializer
from django.contrib.auth import authenticate 
from django.db import IntegrityError
from company_management.renderers import ErrorRenderer 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User , Companies , Departments
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
  renderer_classes = [ErrorRenderer]
  def post(self, request, format=None):
    print("----request.data----", request.data)
    serializer = UserRegistrationSerializer(data=request.data)
    # print("---serializer---", serializer)
    if serializer.is_valid(raise_exception=True):
          user = serializer.save()
          token = get_tokens_for_user(user)
          return Response({'status': status.HTTP_201_CREATED,'success': True, 'message':'Registration Successful', 'data': {'token': token}}, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
       serializer = UserLoginSerializer(data=request.data)
       try:
            if  serializer.is_valid(raise_exception=True):
                    user = serializer.validated_data['user']
                    token = get_tokens_for_user(user)  
                    return Response({'status': status.HTTP_200_OK, 'success': True, 'token': token}, status=status.HTTP_200_OK)
       except ValidationError as e :
            return Response({'status': status.HTTP_400_BAD_REQUEST,'success': False, 'message':e.detail},status=status.HTTP_400_BAD_REQUEST)

    
class UserProfileView(APIView):
    renderer_classes = [ErrorRenderer]
    permission_classes = [IsAuthenticated] 

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'User Profile', 'data': serializer.data})
    

class UserListView(APIView):
    permission_classes = [IsAuthenticated]  
    renderer_classes = [ErrorRenderer]
    def get(self, request, format=None):
        queryset = User.objects.filter(is_active=True)
        serializer = UserListSerializer(queryset, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'User List', 'data': serializer.data})
    

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [ErrorRenderer]

    def get(self, request, id, format=None):
        try:
            user = get_object_or_404(User, id=id)
            serializer = UserProfileSerializer(user)
            return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'User Detail', 'data': serializer.data})
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            serializer = UserDetailSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                if serializer.validated_data:  
                    serializer.save()
                    return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'User details updated successfully'})
                else:  
                    return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'No changes to update'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'errors': {'detail': 'User not found'}})

    def delete(self, request, id, format=None):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, 'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class CompanyView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [ErrorRenderer]
    
    def get(self, request):
        companies = Companies.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'data': serializer.data })

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        print('=-=-=-=-=-=-=-=-' , request.data)
        if serializer.is_valid():
            print('=-=-=-=-=-=-=-=-',request.user.id)
            serializer.validated_data['user_id'] = request.user.id
            serializer.save()
            return Response({'status': status.HTTP_201_CREATED, 'success' : True , 'data': serializer.data })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [ErrorRenderer]
    def get(self, request, id, format=None):
        try:
            company = get_object_or_404(Companies, id=id)
            serializer = CompanyDetailSerializer(company)
            return Response({'status': status.HTTP_200_OK, 'success': True,'data': serializer.data})
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'errors': {'detail': 'Company not found'}}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            serializer = CompanyDetailSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                if serializer.validated_data:  
                    serializer.save()
                    return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Company details updated successfully'})
                else:  
                    return Response({'status': status.HTTP_200_OK, 'success': True, 'errors': {'detail': 'No changes to update'}})
            return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'errors': {'detail': 'Company not found'}})


    def delete(self, request, id, format=None):
        try:
            company = get_object_or_404(Companies, id=id)
            company.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True ,'message' : 'Delete Company successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'errors': {'detail': 'Company not found'}})
        

class DepartmentView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [ErrorRenderer]

    def get(self, request):
        companies = Departments.objects.all()
        serializer = DepartmentSerializer(companies, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'data': {'Department':serializer.data}})

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'success': True, 'data': {'Department':serializer.data}}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            error_message = "Department with the same name already exists for this company."
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'error': {'detail':error_message}}, status=status.HTTP_404_NOT_FOUND)
    

class DepartmentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [ErrorRenderer]
    def get(self, request, id, format=None):
        try:
            departments = get_object_or_404(Departments, id=id)
            serializer = DepartmentDetailSerializer(departments)
            return Response({'status': status.HTTP_200_OK, 'success': True,'data': serializer.data})
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'errors': {'detail': 'department not found'}}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, id):
        try:
            departments = get_object_or_404(Departments, id=id)
            serializer = DepartmentDetailSerializer(departments , data=request.data, partial=True)
            if serializer.is_valid():
                if serializer.validated_data:  
                    serializer.save()
                    return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'department details updated successfully'})
                else:  
                    return Response({'status': status.HTTP_200_OK, 'success': True, 'errors': {'detail': 'No changes to update'}})
            return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'errors': {'detail': 'department not found'}})


    def delete(self, request, id, format=None):
        try:
            departments = get_object_or_404(Departments, id=id)
            departments.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True , 'message' : 'Delete Company successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'errors': {'detail': 'department not found'}})