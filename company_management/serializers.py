from rest_framework import serializers
from .utils import formatted_timestamp
from .models import User , Company
import pytz


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username' , 'first_name', 'last_name', 'gender' , 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        return User.objects.create_user(password=password, **validated_data)
    

class UserLoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            if '@' in email_or_username:
                user = User.objects.filter(email=email_or_username).first()
            else:
                user = User.objects.filter(username=email_or_username).first()

            if user:
                if user.check_password(password):
                    attrs['user'] = user
                else:
                    raise serializers.ValidationError('Incorrect password.')
            else:
                raise serializers.ValidationError('User not found.')
        else:
            raise serializers.ValidationError('Please provide both email/username and password.')

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email','username','first_name', 'last_name','gender','password','created_at' , 'updated_at']


class UserListSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    class Meta:
        model = User
        fields = ['id', 'email','username','first_name', 'last_name','gender','password','created_at' , 'updated_at']


class UserDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'gender', 'created_at', 'updated_at']


class CompanySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    class Meta:
        model = Company
        fields = '__all__'


class CompanyDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    
    class Meta:
        model = Company
        fields = '__all__'



