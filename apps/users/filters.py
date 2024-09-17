import django_filters
from .models import User
from django import forms
#from company.models import Company

class UserStaffFillter(django_filters.FilterSet):
  email = django_filters.CharFilter(field_name='email',
        lookup_expr='icontains',
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-2/3 sm:w-1/2 py-2 pl-10 border border-gray-300 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Enter email',
        }))
  phone_number = django_filters.CharFilter(field_name='phone_number',
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-1/2 py-2 pl-10 border border-gray-300 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Τηλέφωνο',
        }))
  is_active = django_filters.ChoiceFilter(
        choices=[(True, 'Online'), (False, 'Offline')],
        empty_label='-----',
        label=False,
        widget=forms.Select(attrs={
            'class': 'form-select mt-1 block w-48 border border-gray-300 rounded-lg',  # Tailwind classes
        })
    )

  #company = django_filters.ModelChoiceFilter(queryset=Company.objects.none(), label='Εταιρεία')
  
  class Meta:
    model = User
    fields = ['email','phone_number','is_active']