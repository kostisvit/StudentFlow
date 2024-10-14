from django.contrib import admin
from .models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title','owner_name','address','city','postal_code','country','phone_number','email','is_active','created','modified')
    list_filter = ('title','owner_name')

admin.site.register(Organization,OrganizationAdmin)
