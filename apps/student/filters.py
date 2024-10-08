import django_filters
from .models import Student, Subscription, Course
from organization.models import Organization
from django import forms
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class StudentFilter(django_filters.FilterSet):
    IS_ACTIVE_CHOICES = (
        (True, 'Active'),
        (False, 'Inactive'),
    )
        
    membership_number = django_filters.CharFilter(lookup_expr='icontains',label=False,widget=forms.TextInput(attrs={
            'class': 'block text-center sm:w-1/2 py-2  border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Κωδικός μέλους',
        }))
    organization = django_filters.ModelChoiceFilter(queryset=Organization.objects.none(),label=False,empty_label="---Επιλέξτε Οργανισμό---", widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block border border-gray-300 rounded-lg text-gray-700',  # Tailwind classes
        }))
    last_name = django_filters.CharFilter(field_name='user__last_name', lookup_expr='icontains',label=False,widget=forms.TextInput(attrs={
            'class': 'block   text-center sm:w-1/2 py-2  border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Επώνυμο',
        }))
    phone_number = django_filters.CharFilter(field_name='user__phone_number', lookup_expr='icontains',label=False,widget=forms.TextInput(attrs={
            'class': 'block  text-center sm:w-1/2 py-2  border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Τηλέφωνο',
        }))
    is_active = django_filters.ChoiceFilter(field_name='user__is_active',empty_label="---Κατάσταση---",label=False,choices=IS_ACTIVE_CHOICES,widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block  border border-gray-300 rounded-lg text-gray-700',  # Tailwind classes
        }))
    email = django_filters.CharFilter(field_name='user__email', lookup_expr='icontains',label=False,widget=forms.TextInput(attrs={
            'class': 'block   text-center sm:w-1/2 py-2  border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Email',
        }))
    year = django_filters.NumberFilter(field_name='user__date_joined', lookup_expr='year',label=False,widget=forms.TextInput(attrs={
            'class': 'block   text-center sm:w-1/2 py-2  border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Έτος',
        }))
    
    class Meta:
        model = Student
        fields = ['organization','membership_number','last_name','phone_number','is_active','email','year']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
        if user and hasattr(user, 'organization'):
 
            if user.is_superuser:
                organization = user.organization
                self.filters['organization'].queryset = Organization.objects.all().distinct()
            else:
                self.filters['organization'].queryset = Organization.objects.filter(user__organization=user.organization.id).distinct()




class SubscriptionFilter(django_filters.FilterSet):
    start_date = django_filters.NumberFilter(lookup_expr='year', label=False,widget=forms.TextInput(attrs={
            'class': 'block  text-center sm:w-1/2 py-2  border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm',  # Tailwind classes
            'placeholder': 'Έτος',
        }))
    course = django_filters.ModelChoiceFilter(queryset=Course.objects.all(), label=False,empty_label="---Επιλέξτε Μάθημα---", widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block  border border-gray-300 rounded-lg text-gray-700',  # Tailwind classes
        }))
    user = django_filters.ModelChoiceFilter(queryset=get_user_model().objects.all(),label=False, empty_label="---Επιλέξτε Καθηγητή---", widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block  border border-gray-300 rounded-lg text-gray-700',  # Tailwind classes
        }))
    is_online = django_filters.ChoiceFilter(
        choices=[(True, 'Online'), (False, 'Offline')],
        empty_label="---Κατάσταση---",label=False,widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block  border border-gray-300 rounded-lg text-gray-700',  # Tailwind classes
        })
    )
        
    class Meta:
        model = Subscription
        fields = ['course','user','is_online','start_date']

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'organization'):

            if user.is_superuser:
                organization = user.organization
                self.filters['course'].queryset = Course.objects.all()
                self.filters['user'].queryset = get_user_model().objects.filter(is_staff=True)
            else:
                self.filters['course'].queryset = Course.objects.filter(organization=user.organization.id)
                self.filters['user'].queryset = get_user_model().objects.filter(organization=user.organization.id,is_staff=True)





    