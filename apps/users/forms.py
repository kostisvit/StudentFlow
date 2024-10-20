from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Vacation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from organization.models import Organization
from django.forms import ModelChoiceField,ModelMultipleChoiceField
from .choices import gender_choice
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from student.models import Student, Enrollment, Course
from .validators import validate_file_extension
from .models import Course, Document,EmployeeDocument


UserModel = get_user_model()

# Email authentication, check email if exists
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean_username(self):
        email = self.cleaned_data.get('username')
        if not UserModel.objects.filter(email=email).exists():
            raise ValidationError("Το email δεν υπάρχει, επικοινωνήστε με τον διαχειριστή. ")
        return email

#########################################################################################################

# User New Form
class UserCreationForm(forms.ModelForm):
    organization = ModelChoiceField(queryset=Organization.objects.all(),widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Οργανισμός',required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-700 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6','placeholder': 'YYYY-MM-DD',}),label='Ημ. Γέννησης',required=False)
    gender = forms.ChoiceField(choices=gender_choice,widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Φύλο',required=True)
    first_name = forms.CharField(label='Όνομα', widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=True)
    last_name = forms.CharField(label='Επώνυμο',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=True)
    phone_number = forms.CharField(label='Τηλ. Επικ.',widget=forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),required=True)
    address = forms.CharField(label='Διεύθυνση',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=True)
    city = forms.CharField(label='Πόλη',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    country = forms.CharField(label='Χώρα',initial='Ελλάδα',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    postal_code = forms.CharField(label='ΤΚ',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700' }),required=False)
    is_active = forms.BooleanField(label='Κατάσταση',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}), initial=True,required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off','class':'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),required=True)
    is_staff = forms.BooleanField(initial=True,label='Καθηγητής',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    is_company_owner = forms.BooleanField(label='Ιδιοκτήτης', initial=False, widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    is_student = forms.BooleanField(initial=False,label='Μαθητής',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    courses = ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),
        label='Μαθήματα',
        required=False
    )
    
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('organization','email','first_name','last_name','date_of_birth','phone_number','address','city','postal_code','country','gender','is_active','is_staff','is_company_owner','is_student','courses')

    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # Ensure the password fields are correctly initialized
        if 'password1' not in self.fields:
            self.fields['password1'] = forms.CharField(widget=forms.PasswordInput(), required=False)
        if 'password2' not in self.fields:
            self.fields['password2'] = forms.CharField(widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        # Capture the user from the form arguments
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter courses based on user type
        if user and user.is_superuser:
            # Superuser: Show all courses
            self.fields['courses'].queryset = Course.objects.filter(is_online=True)
        elif user and hasattr(user, 'organization'):
            # Regular user: Only show courses where is_online=True
            self.fields['courses'].queryset = Course.objects.filter(is_online=True, organization=user.organization)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password('password')  # Set your default password here
        if commit:
            user.save()
            is_student = self.cleaned_data.get('is_student')
            student, created = Student.objects.get_or_create(user=user, defaults={'is_student': is_student})
            
            if not created:
                # Update is_student if Member already exists
                student.is_student = is_student
                student.save()
                # Save enrollments for the selected courses
        courses = self.cleaned_data.get('courses')
        if courses:
            for course in courses:
                Enrollment.objects.get_or_create(user=user, course=course)
        return user

#########################################################################################################

# Student - User Change Form
class UserChangeForm(forms.ModelForm):
    organization = ModelChoiceField(queryset=Organization.objects.all(),widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Οργανισμός',required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-700 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6','placeholder': 'YYYY-MM-DD',}),label='Ημ. Γέννησης',required=False)
    gender = forms.ChoiceField(choices=gender_choice,widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Φύλο')
    first_name = forms.CharField(label='Όνομα', widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}))
    last_name = forms.CharField(label='Επώνυμο',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}))
    phone_number = forms.CharField(label='Τηλ. Επικ.',widget=forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),required=False)
    address = forms.CharField(label='Διεύθυνση',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    city = forms.CharField(label='Πόλη',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    country = forms.CharField(label='Χώρα',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    postal_code = forms.CharField(label='ΤΚ',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700' }),required=False)
    is_active = forms.BooleanField(label='Κατάσταση',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}), initial=True,required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off','class':'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    is_staff = forms.BooleanField(initial=True,label='Καθηγητής',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    is_company_owner = forms.BooleanField(label='Ιδιοκτήτης', initial=False, widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    is_student = forms.BooleanField(initial=False,label='Μαθητής',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    courses = ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),
        label='Μαθήματα',
        required=False
    )
        
    class Meta():
        model = User
        exclude = ['user',] 
        fields = ('organization','email','first_name','last_name','date_of_birth','phone_number','address','city','postal_code','country','gender','is_active','is_staff','is_company_owner','is_student','courses')


    def __init__(self, *args, **kwargs):
        # Get the user instance from kwargs (if it's provided)
        user = kwargs.get('instance', None)
        super(UserChangeForm, self).__init__(*args, **kwargs)
        # Populate the 'courses' field with the user's current enrollments
        if self.instance and self.instance.pk:
            enrolled_courses = Course.objects.filter(enrollment__user=self.instance)
            self.fields['courses'].initial = enrolled_courses
            
        # Pre-fill the organization field from the Student model
        if user and hasattr(user, 'student'):
            self.fields['is_student'].initial = user.student.is_student

    def save(self, commit=True):
        # Get the user instance
        user = super().save(commit=False)

        # Save the user if commit=True
        if commit:
            user.save()

        # Get the selected courses
        selected_courses = self.cleaned_data['courses']

        # Clear the existing enrollments for the user
        Enrollment.objects.filter(user=user).delete()

        # Create new enrollments for the selected courses
        for course in selected_courses:
            Enrollment.objects.get_or_create(user=user, course=course)

        return user

#########################################################################################################

class VacationStaffForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=get_user_model().objects.filter(is_staff=True),label=False,empty_label='---Επέλεξε Καθηγητή---',widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-700 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6','placeholder': 'YYYY-MM-DD',}),label='Έναρξη',required=True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-700 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6','placeholder': 'YYYY-MM-DD',}),label='Λήξη',required=True)
    
    class Meta:
        model = Vacation
        fields = ('user','start_date','end_date')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VacationStaffForm, self).__init__(*args, **kwargs)
        if user and user.is_superuser:
            self.fields['user'].queryset = get_user_model().objects.filter(is_staff=True,is_active=True).order_by('last_name')
        elif user and hasattr(user, 'organization'):
            # Ensure that the 'user' field (teachers) is always ordered by last name
            self.fields['user'].queryset = get_user_model().objects.filter(is_staff=True,is_active=True,organization=user.organization).order_by('last_name')
            
    def save(self, commit=True):
        # Call the superclass's save method to handle the default saving behavior
        vacation = super().save(commit=False)
        
        # Add any additional processing or logic here
        # For example, you can set some additional fields on the vacation instance if needed
        
        if commit:
            vacation.save()  # Save the instance to the database
        
        return vacation


#########################################################################################################


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
    
#########################################################################################################    


class StudentFileForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all(),widget=forms.Select(attrs={'class': 'form-control'}), label="Select User",required=True)
    course = forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}), label="Select Course",required=True)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=True)
    filename = forms.CharField(label='Όνομα αρχείου',required=False)

    class Meta:
        model = Document
        fields = ['user', 'file']


    def __init__(self, *args, **kwargs):
        logged_in_user = kwargs.pop('logged_in_user', None)
        super().__init__(*args, **kwargs)

        # Apply different queryset based on the logged-in user
        if logged_in_user and logged_in_user.is_superuser:
            self.fields['user'].queryset = get_user_model().objects.filter(is_staff=False, is_active=True)
            self.fields['course'].queryset = Course.objects.all()
        else:
            self.fields['user'].queryset = get_user_model().objects.filter(organization=logged_in_user.organization, is_staff=False, is_active=True)
            self.fields['course'].queryset = Course.objects.filter(is_online=True,organization=logged_in_user.organization)

    def clean_file(self):
        files = self.files.getlist('file')  # Get the list of uploaded files
        for file in files:
            validate_file_extension(file)  # Validate each file individually
        return files

#########################################################################################################   

class StaffFileForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select User",
        required=True
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Course",
        required=True
    )
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': False}),
        required=True
    )
    filename = forms.CharField(label='Όνομα αρχείου', required=False)

    class Meta:
        model = EmployeeDocument
        fields = ['user', 'file']

    def __init__(self, *args, **kwargs):
        logged_in_user = kwargs.pop('logged_in_user', None)
        super().__init__(*args, **kwargs)

        # Apply different queryset based on the logged-in user
        if logged_in_user and logged_in_user.is_superuser:
            self.fields['user'].queryset = get_user_model().objects.filter(is_staff=True, is_active=True)
            self.fields['course'].queryset = Course.objects.all()
        else:
            self.fields['user'].queryset = get_user_model().objects.filter(organization=logged_in_user.organization, is_staff=True,is_active=True)
            self.fields['course'].queryset = Course.objects.filter(is_online=True)

    def clean_file(self):
        files = self.files.getlist('file')  # Get list of uploaded files
        if not files:
            raise ValidationError("Please upload at least one file.")

        for file in files:
            if not file:
                raise ValidationError("The provided file is not valid.")
            
            # Assuming you have validate_file_extension defined
            from .validators import file_size_validator

            file_size_validator(file)

        return files

#########################################################################################################   
