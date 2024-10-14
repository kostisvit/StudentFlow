from django import forms 
from django.forms import ModelForm
from .models import Organization


class OrganizationForm(ModelForm):
    
    class Meta:
        model = Organization
        fields = '__all__'
        exclude = ['created']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the field not required
        self.fields['address'].required = False
        self.fields['city'].required = False
        self.fields['postal_code'].required = False
        self.fields['country'].required = False
        self.fields['phone_number'].required = False