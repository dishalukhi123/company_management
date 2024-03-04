from django.contrib import admin
from .models import User , Company
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'gender', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'gender', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()

# Unregister the existing UserAdmin if it's registered
admin.site.unregister(User)

# Register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'type', 'created_at', 'updated_at')
    search_fields = ['name', 'location', 'type']
    list_filter = ['type']
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Company, CompanyAdmin)

