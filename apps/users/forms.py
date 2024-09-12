from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
#from company.models import Company
from django.forms import ModelChoiceField
from datetime import date
from .choices import gender_choice
#from members.models import Member
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

UserModel = get_user_model()

# Email authentication, check email if exists
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean_username(self):
        email = self.cleaned_data.get('username')
        if not UserModel.objects.filter(email=email).exists():
            raise ValidationError("Το email δεν υπάρχει, επικοινωνήστε με τον διαχειριστή. ")
        return email


# Custom User-Student New Form
class UserCreationForm(forms.ModelForm):
    #company = ModelChoiceField(queryset=Company.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}),label='Εταιρεία',required=False)
    date_joined = forms.DateField(initial=date.today,widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),label='Ημ. Εγγραφης')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),label='Ημ. Γέννησης')
    gender = forms.ChoiceField(choices=gender_choice,widget=forms.Select(attrs={'class': 'form-control'}),label='Φύλο')
    first_name = forms.CharField(label='Όνομα')
    last_name = forms.CharField(label='Επώνυμο')
    phone_number = forms.CharField(label='Τηλ. Επικ.',required=False)
    address = forms.CharField(label='Διεύθυνση',required=False)
    city = forms.CharField(label='Πόλη',required=False)
    country = forms.CharField(label='Χώρα',required=False)
    postal_code = forms.CharField(label='ΤΚ')
    is_active = forms.BooleanField(label='Κατάσταση', initial=True,required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off','class': 'custom-email-field'}))
    is_student = forms.BooleanField(initial=True,label='Μαθητής',required=False)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email','first_name','last_name','date_joined','date_of_birth','phone_number','address','city','postal_code','country','gender','is_active','is_student')

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['is_student'].widget.attrs['disabled'] = True

    
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(CustomUserCreationForm, self).__init__(*args, **kwargs)
    #     if user:
    #         if user.is_superuser:
    #             self.fields['company'].queryset = Company.objects.all()
    #         else:
    #             self.fields['company'].queryset = Company.objects.filter(id=user.company.id)


    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password('password')  # Set your default password here
    #     if commit:
    #         user.save()
    #         is_student = self.cleaned_data.get('is_student')
    #         member, created = Member.objects.get_or_create(user=user, defaults={'is_student': is_student})
            
    #         if not created:
    #             # Update is_student if Member already exists
    #             member.is_student = is_student
    #             member.save()
    #     return user

# Custom User Change Form
class UserChangeForm(UserChangeForm):
    #company = ModelChoiceField(queryset=Company.objects.order_by('name'),widget=forms.Select(attrs={'class': 'form-control'}),label='Εταιρεία')
    date_joined = forms.DateField(initial=date.today,widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),label='Ημ. Εγγραφης')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),label='Ημ. Γέννησης')
    gender = forms.ChoiceField(choices=gender_choice,widget=forms.Select(attrs={'class': 'form-control'}),label='Φύλο')
    first_name = forms.CharField(label='Όνομα')
    last_name = forms.CharField(label='Επώνυμο')
    phone_number = forms.CharField(label='Τηλ. Επικ.')
    address = forms.CharField(label='Διεύθυνση')
    city = forms.CharField(label='Πόλη')
    country = forms.CharField(label='Χώρα')
    postal_code = forms.CharField(label='ΤΚ')
    is_active = forms.BooleanField(label='Κατάσταση',required=False, initial=True)
    is_student = forms.BooleanField(initial=True,label='Μαθητής',required=False)
    
    class Meta:
        model = User
        fields = ('email','first_name','last_name','date_joined','date_of_birth','phone_number','address','city','postal_code','country','gender','is_active','is_student')
 
 
 # Custom Staff New Form
class UserStaffCreationForm(forms.ModelForm):
    #company = ModelChoiceField(queryset=Company.objects.order_by('name'),widget=forms.Select(attrs={'class': 'form-control'}),label='Εταιρεία')
    date_joined = forms.DateField(initial=date.today,widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),label='Ημ. Εγγραφης')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),label='Ημ. Γέννησης')
    gender = forms.ChoiceField(choices=gender_choice,widget=forms.Select(attrs={'class': 'form-control'}),label='Φύλο')
    first_name = forms.CharField(label='Όνομα')
    last_name = forms.CharField(label='Επώνυμο')
    phone_number = forms.CharField(label='Τηλ. Επικ.')
    address = forms.CharField(label='Διεύθυνση')
    city = forms.CharField(label='Πόλη')
    country = forms.CharField(label='Χώρα')
    postal_code = forms.CharField(label='ΤΚ')
    is_active = forms.BooleanField(label='Ενεργός', initial=True,required=False)
    is_staff = forms.BooleanField(label='Υπάλληλος', initial=True, required=False)
    is_company_owner = forms.BooleanField(label='Ιδιοκτήτης', initial=False, required=False)
    
    class Meta:
        model = User
        fields = ('email','first_name','last_name','date_joined','date_of_birth','phone_number','address','city','postal_code','country','gender','is_active','is_staff','is_company_owner')
        # labels = {
        #     'course': 'Ειδικότητα',  # Set the label for the ManyToManyField
        # }
        # widgets = {
        #     'course': forms.CheckboxSelectMultiple(), 
        # }
    
    def __init__(self, *args, **kwargs):
        super(UserStaffCreationForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].widget.attrs['disabled'] = True

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(UserStaffCreationForm, self).__init__(*args, **kwargs)
    #     if user:
    #         if user.is_superuser:
    #             self.fields['company'].queryset = Company.objects.all()
    #         else:
    #             self.fields['company'].queryset = Company.objects.filter(id=user.company.id)

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password('password')  # Set your default password here
    #     if commit:
    #         user.save()
    #         is_student = self.cleaned_data.get('is_student')
    #         member, created = Member.objects.get_or_create(user=user, defaults={'is_student': is_student})
            
    #         if not created:
    #             # Update is_student if Member already exists
    #             member.is_student = is_student
    #             member.save()
    #     return user

# Email Authentication
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Λάθος email ή password. Προσπαθήστε πάλι."
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    
    




# from .validators import validate_file_extension
# from .models import Course


# class MultipleUserFileForm(forms.Form):
#     user = forms.ModelChoiceField(queryset=CustomUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}), label="Select User")
#     course = forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}), label="Select Course")
#     file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
#     filename = forms.CharField(label='Όνομα αρχείου',required=False)


#     def __init__(self, *args, **kwargs):
#         logged_in_user = kwargs.pop('logged_in_user', None)
#         super().__init__(*args, **kwargs)

#         # Apply different queryset based on the logged-in user
#         if logged_in_user and logged_in_user.is_superuser:
#             self.fields['user'].queryset = CustomUser.objects.all()
#             self.fields['course'].queryset = Course.objects.all()
#         else:
#             self.fields['user'].queryset = CustomUser.objects.filter(
#                 company=logged_in_user.company, is_staff=False
#             )
#             self.fields['course'].queryset = Course.objects.filter(company=logged_in_user.company.id)

#         # Add Bootstrap error class handling
#         for field_name in self.fields:
#             field = self.fields[field_name]
#             if self.errors.get(field_name):
#                 field.widget.attrs.update({'class': 'form-control is-invalid'})
#             else:
#                 field.widget.attrs.update({'class': 'form-control'})

#     def clean_file(self):
#         files = self.files.getlist('file')  # Get the list of uploaded files
#         for file in files:
#             validate_file_extension(file)  # Validate each file individually
#         return files


