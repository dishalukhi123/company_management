from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from company_management.serializers import UserRegistrationSerializer , UserLoginSerializer , UserProfileSerializer , UserListSerializer , UserDetailSerializer , UserUpdateSerializer
from django.contrib.auth import authenticate 
from company_management.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User
from django.shortcuts import get_object_or_404



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
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
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Login Success', 'data': {'token': token}}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    
    
    
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

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def get(self, request, id, format=None):
        user = self.get_object(id)
        if user is not None:
            serializer = UserProfileSerializer(user)
            return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'User Detail', 'data': serializer.data})
        else:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)





class UserUpdateView(APIView):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)

    def patch(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200, 'success': True, 'message': 'User details updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDeleteView(APIView):
    def delete(self, request, id, format=None):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, 'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
