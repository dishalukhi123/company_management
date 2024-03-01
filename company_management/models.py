import pytz
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
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
        db_table = 'user'

    def formatted_created_at(self):
        local_timezone = pytz.timezone('Asia/Kolkata')
        local_created_at = self.created_at.astimezone(local_timezone)
        return local_created_at.strftime("%I:%M %p %A, %b %d, %Y")
    
    def formatted_updated_at(self):
        local_timezone = pytz.timezone('Asia/Kolkata')
        local_updated_at = self.updated_at.astimezone(local_timezone)
        return local_updated_at.strftime("%I:%M %p %A, %b %d, %Y")

class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_admin')

admin.site.register(User, UserModelAdmin)
