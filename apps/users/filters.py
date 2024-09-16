import django_filters
from .models import User
#from company.models import Company

class UserStaffFillter(django_filters.FilterSet):
  email = django_filters.CharFilter(lookup_expr='icontains',label="Email")
  is_active = django_filters.ChoiceFilter(
        choices=[(True, 'Online'), (False, 'Offline')],
        empty_label='Any',
        label='Status'
    )
  phone_number = django_filters.CharFilter(field_name='phone_number', lookup_expr='icontains',label="Τηλέφωνο")
  #company = django_filters.ModelChoiceFilter(queryset=Company.objects.none(), label='Εταιρεία')
  
  class Meta:
    model = User
    fields = ['email','is_active','phone_number']