import django_filters
from .models import User, Document, Vacation
from student.models import Course
from django import forms
from django.contrib.auth import get_user_model


UserModel = get_user_model()
#from company.models import Company

class UserStaffFillter(django_filters.FilterSet):
  email = django_filters.CharFilter(field_name='email',
        lookup_expr='icontains',
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block  text-center sm:w-1/2 py-2  border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Enter email',
        }))
  phone_number = django_filters.CharFilter(field_name='phone_number',
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block  text-center sm:w-1/2 py-2  border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Τηλέφωνο',
        }))
  is_active = django_filters.ChoiceFilter(
        choices=[(True, 'Online'), (False, 'Offline')],
        empty_label="---Κατάσταση---",
        label=False,
        widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block  border border-gray-300 rounded-lg text-gray-700',  # Tailwind classes
        })
    )

  #company = django_filters.ModelChoiceFilter(queryset=Company.objects.none(), label='Εταιρεία')
  
  class Meta:
    model = User
    fields = ['email','phone_number','is_active']



class VacationFilter(django_filters.FilterSet):
        user = django_filters.ModelChoiceFilter(queryset=get_user_model().objects.filter(is_staff=True),label=False, empty_label="---Επιλέξτε Καθηγητή---", widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block  border border-gray-300 rounded-lg text-gray-700',  # Tailwind classes
        }))
        
        year = django_filters.NumberFilter(field_name="start_date", lookup_expr='year',label=False,widget=forms.TextInput(attrs={
            'class': 'block   text-center sm:w-1/2 py-2  border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Έτος',
        }))
        
        class Meta:
            model = Vacation
            fields = ['user','year']

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            
            # Set queryset for organization and user based on the provided user
            if user and hasattr(user, 'organization'):
                if user.is_superuser:
                    # Superuser can see all organizations and users
                    self.filters['user'].queryset = User.objects.filter(is_staff=True).distinct()
                else:
                    self.filters['user'].queryset = User.objects.filter(
                        organization=user.organization,
                        is_staff=True  # Assuming you want to filter for staff users only
                    ).distinct()
    


class DocumentFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(queryset=get_user_model().objects.filter(is_staff=True),label=False, empty_label="---Επιλέξτε Καθηγητή---", widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block  border border-gray-300 rounded-lg text-gray-700',  # Tailwind classes
        }))
        
    course = django_filters.ModelChoiceFilter(queryset=Course.objects.all(), label=False,empty_label="---Επιλέξτε Μάθημα---", widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block  border border-gray-300 rounded-lg text-gray-700',  # Tailwind classes
        }))
        
    class Meta:
        model = Document
        fields = ['user','course']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
            
            # Set queryset for organization and user based on the provided user
        if user and hasattr(user, 'organization'):
            if user.is_superuser:
                    # Superuser can see all organizations and users
                self.filters['course'].queryset = Course.objects.all().distinct()
                self.filters['user'].queryset = User.objects.filter(is_staff=True).distinct()
            else:
                    # Non-superuser can only see their own organization's data
                self.filters['course'].queryset = Course.objects.filter(
                    organization=user.organization # Assuming the Organization model has a reverse relation to User
                ).distinct()
                    
                self.filters['user'].queryset = User.objects.filter(
                    organization=user.organization,
                    is_staff=True  # Assuming you want to filter for staff users only
                ).distinct()