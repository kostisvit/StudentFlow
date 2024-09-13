import django_filters
from .models import Student
from organization.models import Organization
from django import forms
from users.models import User



class StudentFilter(django_filters.FilterSet):
    IS_ACTIVE_CHOICES = (
 # Optional: for no selection
        (True, 'Active'),
        (False, 'Inactive'),
    )
        
    membership_number = django_filters.CharFilter(lookup_expr='icontains',label="Κωδικός Μέλους")
    organization = django_filters.ModelChoiceFilter(queryset=Organization.objects.none(), label='Εταιρεία')
    last_name = django_filters.CharFilter(field_name='user__last_name', lookup_expr='icontains',label="Επώνυμο")
    phone_number = django_filters.CharFilter(field_name='user__phone_number', lookup_expr='icontains',label="Τηλέφωνο")
    is_active = django_filters.ChoiceFilter(field_name='user__is_active',label="Κατάσταση",choices=IS_ACTIVE_CHOICES,)
    email = django_filters.CharFilter(field_name='user__email', lookup_expr='icontains',label="Email")
    year = django_filters.NumberFilter(field_name='user__date_joined', lookup_expr='year',label='Έτος')
    
    class Meta:
        model = Student
        fields = {
            'membership_number': ['icontains'],
            }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
        if user and hasattr(user, 'organization'):
                # Assuming CustomUser has a direct company field
            if user.is_superuser:
                organization = user.organization
                self.filters['organization'].queryset = Organization.objects.all().distinct()
            else:
                self.filters['organization'].queryset = Organization.objects.filter(user__organization=user.organization.id).distinct()