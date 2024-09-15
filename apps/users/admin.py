from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active','gender','is_company_owner')
    list_filter = ('is_staff', 'is_active')
    readonly_fields = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth','phone_number','postal_code','address','city','country','gender',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active','groups','is_company_owner', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email',  'is_staff', 'is_active','is_company_owner','date_of_birth','phone_number','address','city','country','gender','postal_code','groups', 'user_permissions')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    

admin.site.register(User, UserAdmin)


