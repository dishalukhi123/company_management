from rest_framework import serializers
from .utils import formatted_timestamp
from .models import User , Companies , Departments , Employees
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
        email = attrs.get('email')
        print("--attrs---", attrs)
        errors = {}
        # if password != confirm_password:
        #     errors['password'] = ["Password and Confirm Password don't match"]

        if User.objects.filter(email=email).exists():
            errors['email'] = ["User with this email already exists."]

        if errors:
            print("---errors---", errors)
            raise serializers.ValidationError(errors)

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
    companies = serializers.SerializerMethodField()


    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    
    def get_companies(self, obj):
        user_companies = Companies.objects.filter(user_id=obj.id)
        serializer = CompanySerializer(user_companies, many=True)
        return serializer.data
    
    class Meta:
        model = User
        fields = ['id', 'email','username','first_name', 'last_name','gender','password','created_at' , 'updated_at' , 'companies']


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
        model = Companies
        fields = ['id', 'name', 'about', 'type', 'created_at', 'updated_at', 'active' ,'user_id' ,'city', 'state', 'country' , 'other_location' ]


class CompanyDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)


    class Meta:
        model = Companies
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(queryset=Companies.objects.all(),source='company', write_only=True)
    company=CompanySerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    
    
    def to_internal_value(self, data):
        try:
            company_id = data.get('company_id')
            company = Companies.objects.get(pk=company_id)
            validated_data = super().to_internal_value(data)
            validated_data['company_id'] = company.pk
            return validated_data
        except (KeyError, ValueError, Companies.DoesNotExist):
            raise serializers.ValidationError({"company_id": ["Invalid company_id - Company does not exist."]})



    class Meta:
        model = Departments
        fields = '__all__'

        
class CompanyEmployeeSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()

    def get_employees(self, obj):
        company_employees = Employees.objects.filter(company_id=obj.id)
        serializer = EmployeeSerializer(company_employees, many=True)
        return serializer.data

    class Meta:
        model = Companies
        fields = ['id', 'name', 'about', 'employees']


class DepartmentDetailSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(queryset=Companies.objects.all(),source='company', write_only=True )
    company=CompanySerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    
    class Meta:
        model = Departments
        fields = '__all__'

        
class EmployeeSerializer(serializers.ModelSerializer):
    department_id = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all(), source='department', write_only=True)
    department = serializers.SerializerMethodField()
    company_id = serializers.PrimaryKeyRelatedField(queryset=Companies.objects.all(),source='company', write_only=True )
    company=CompanySerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_department(self, instance):
        department = instance.department
        return {
            "id": department.id,
            "name": department.name,
            "description": department.description,
        }

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists in the users table.")
        return value

    class Meta:
        model = Employees
        fields = '__all__'

        

class EmployeeDetailSerializer(serializers.ModelSerializer):
    department_id = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all(), source='department', write_only=True)
    department = serializers.SerializerMethodField()
    company_id = serializers.PrimaryKeyRelatedField(queryset=Companies.objects.all(),source='company', write_only=True )
    company=CompanySerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_department(self, instance):
        department = instance.department
        return {
            "id": department.id,
            "name": department.name,
            "description": department.description,
        }

    def get_created_at(self, instance):
        return formatted_timestamp(instance.created_at)

    def get_updated_at(self, instance):
        return formatted_timestamp(instance.updated_at)
    

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists in the User table.")
        elif Employees.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
            raise serializers.ValidationError("Email already exists in the Employees table.")
        return value


    class Meta:
        model = Employees
        fields = '__all__'



        



