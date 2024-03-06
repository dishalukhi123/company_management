from django.contrib import admin
from .models import User, Company

class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_admin')

admin.site.register(User, UserModelAdmin)


class CompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Company, CompanyAdmin)
