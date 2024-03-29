from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError



class UserManager(BaseUserManager):
    def create_user(self, email, username=None, first_name='', last_name='', gender='', password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, first_name='', last_name='', gender='', password=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'gender']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'users'



class Companies(models.Model):
    TYPE_CHOICES = (
        ('private company', 'Private Company'),
        ('associate company', 'Associate company'),
        ('government', 'Government'),
    )
    name = models.CharField(max_length=100 , unique = True )
    city = models.CharField(max_length=100) 
    state = models.CharField(max_length=100) 
    country = models.CharField(max_length=100) 
    about = models.CharField(max_length = 200)
    type = models.CharField(max_length = 40 , choices=TYPE_CHOICES) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) 
    user_id = models.IntegerField(blank=True, null=True)

    
    class Meta:
        db_table = 'companies'

class Departments(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'company'], name='unique_department_per_company')]
        db_table = 'departments'
    

class Employees(models.Model):
    POSITION_CHOICES = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('analyst', 'Analyst'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    salary = models.DecimalField(max_digits=10 , decimal_places=2)
    address = models.CharField(max_length=255)
    about = models.TextField(max_length=255)
    phone_number = models.CharField(max_length=10 , unique=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'employees'
