from django.contrib import admin
from .models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title','owner_name','address','city','postal_code','country','phone_number','email','is_active','created','modified')
    list_filter = ('title','owner_name')
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super(OrganizationAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)
        
        # Make the `description` field optional in the admin form
        if db_field.name == 'address':
            formfield.required = False
        if db_field.name == 'city':
            formfield.required = False
        if db_field.name == 'postal_code':
            formfield.required = False
        if db_field.name == 'country':
            formfield.required = False

        return formfield

admin.site.register(Organization,OrganizationAdmin)
