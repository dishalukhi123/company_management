from rest_framework import serializers
from .models import User
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
    
    

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']



class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email','username','first_name', 'last_name','gender','password','created_at' , 'updated_at']


class UserListSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def formatted_timestamp(self, timestamp):
        local_timezone = pytz.timezone('Asia/Kolkata')
        local_time = timestamp.astimezone(local_timezone)
        return local_time.strftime("%I:%M %p %A, %b %d, %Y")

    def get_created_at(self, instance):
        return self.formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return self.formatted_timestamp(instance.updated_at)
    class Meta:
        model = User
        fields = ['id', 'email','username','first_name', 'last_name','gender','password','created_at' , 'updated_at']


class UserDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def formatted_timestamp(self, timestamp):
        local_timezone = pytz.timezone('Asia/Kolkata')
        local_time = timestamp.astimezone(local_timezone)
        return local_time.strftime("%I:%M %p %A, %b %d, %Y")

    def get_created_at(self, instance):
        return self.formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return self.formatted_timestamp(instance.updated_at)
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'gender', 'created_at', 'updated_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'gender']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance



