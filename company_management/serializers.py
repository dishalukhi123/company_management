from rest_framework import serializers
from .utils import formatted_timestamp
from .models import User , Company , Department
import pytz


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username' , 'first_name', 'last_name', 'gender' , 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        errors = {}
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password', None) 
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
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'gender', 'created_at', 'updated_at']


class CompanySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    other_location  = serializers.SerializerMethodField()
 
    def get_created_at(self, obj):
        return formatted_timestamp(obj.created_at)

    def get_updated_at(self, obj):
        return formatted_timestamp(obj.updated_at)
    
        
    def get_other_location(self, obj):
        print('+++++++++++++++++++',obj.city)
        return f'{obj.city},{obj.state},{obj.country}'
        
    class Meta:
        model = Company
        fields = ['id', 'name', 'about', 'type', 'created_at', 'updated_at', 'active' ,'user_id' ,'city', 'state', 'country' , 'other_location' ]



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


class DepartmentSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(source='company.id', read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'company_id','created_at', 'updated_at']


class DepartmentDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'company_id','created_at', 'updated_at']

        



