from django import forms
from datetime import date
from django.forms import ModelForm,ModelChoiceField
from .models import Subscription, Course, Student
from organization.models import Organization
from users.choices import gender_choice
from django.contrib.auth import get_user_model

UserModel = get_user_model()


# Student Create View
class StudentCreationForm(forms.ModelForm):
    organization = ModelChoiceField(queryset=Organization.objects.all(),widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Οργανισμός',required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6','placeholder': 'YYYY-MM-DD',}),label='Ημ. Γέννησης',required=True)
    gender = forms.ChoiceField(choices=gender_choice,widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Φύλο',required=True)
    first_name = forms.CharField(label='Όνομα', widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=True)
    last_name = forms.CharField(label='Επώνυμο',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=True)
    phone_number = forms.CharField(label='Τηλ. Επικ.',widget=forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),required=True)
    address = forms.CharField(label='Διεύθυνση',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    city = forms.CharField(label='Πόλη',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    country = forms.CharField(label='Χώρα',initial='Ελλάδα',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    postal_code = forms.CharField(label='ΤΚ',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}))
    is_active = forms.BooleanField(label='Κατάσταση',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}), initial=True,required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off','class':'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    #is_staff = forms.BooleanField(initial=True,label='Καθηγητής',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    is_student = forms.BooleanField(initial=True,label='Μαθητής',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    class Meta:
        model = get_user_model()
        fields = ('organization','email','first_name','last_name','date_of_birth','phone_number','address','city','postal_code','country','gender','is_active','is_student')

    
    def __init__(self, *args, **kwargs):
        super(StudentCreationForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].widget.attrs['disabled'] = True

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(StudentCreationForm, self).__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                self.fields['organization'].queryset = Organization.objects.all()
            else:
                self.fields['organization'].queryset = Organization.objects.filter(id=user.organization.id)


    def save(self, commit=True):
        # Save the User model first, without committing to the database yet
        user = super().save(commit=False)

        # Set a default password for the user
        default_password = "defaultpassword123"  # Set your default password here
        user.set_password(default_password)

        # Check if commit is True, then save the user instance
        if commit:
            user.save()

        # Create or update the related Student profile
        is_student = self.cleaned_data.get('is_student', True)
        student_profile, created = Student.objects.get_or_create(user=user)
        student_profile.is_student = is_student
        student_profile.save()

        return user



# Student update form
class StudentUserChangeForm(forms.ModelForm):
    organization = ModelChoiceField(queryset=Organization.objects.all(),widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Οργανισμός',required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6','placeholder': 'YYYY-MM-DD',}),label='Ημ. Γέννησης',required=True)
    gender = forms.ChoiceField(choices=gender_choice,widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Φύλο')
    first_name = forms.CharField(label='Όνομα', widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}))
    last_name = forms.CharField(label='Επώνυμο',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}))
    phone_number = forms.CharField(label='Τηλ. Επικ.',widget=forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),required=False)
    address = forms.CharField(label='Διεύθυνση',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    city = forms.CharField(label='Πόλη',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    country = forms.CharField(label='Χώρα',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    postal_code = forms.CharField(label='ΤΚ',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}))
    is_active = forms.BooleanField(label='Κατάσταση',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}), initial=True,required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off','class':'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    is_student = forms.BooleanField(label='Μαθητής',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)

    class Meta:
        model = Student
        exclude = ['user',] 
        fields = ('organization','email','first_name','last_name','date_of_birth','phone_number','address','city','postal_code','country','gender','is_active','is_student')

    def __init__(self, *args, **kwargs):
        super(StudentUserChangeForm, self).__init__(*args, **kwargs)
        # Populate the first_name field with the value from the related User model
        if self.instance and self.instance.pk:
            self.fields['organization'].initial = self.instance.user.organization
            self.fields['date_of_birth'].initial = self.instance.user.date_of_birth
            self.fields['gender'].initial = self.instance.user.gender
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['phone_number'].initial = self.instance.user.phone_number
            self.fields['address'].initial = self.instance.user.address
            self.fields['city'].initial = self.instance.user.city
            self.fields['country'].initial = self.instance.user.country
            self.fields['postal_code'].initial = self.instance.user.postal_code
            self.fields['is_active'].initial = self.instance.user.is_active
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        student = super(StudentUserChangeForm, self).save(commit=False)
        # Save the first name back to the related User model
        student.user.organization = self.cleaned_data['organization']
        student.user.date_of_birth = self.cleaned_data['date_of_birth']
        student.user.gender = self.cleaned_data['gender']
        student.user.first_name = self.cleaned_data['first_name']
        student.user.last_name = self.cleaned_data['last_name']
        student.user.phone_number = self.cleaned_data['phone_number']
        student.user.address = self.cleaned_data['address']
        student.user.city = self.cleaned_data['city']
        student.user.country = self.cleaned_data['country']
        student.user.postal_code = self.cleaned_data['postal_code']
        student.user.is_active = self.cleaned_data['is_active']
        student.user.email = self.cleaned_data['email']
        if commit:
            student.user.save()
            student.save()
        return student




# Subscriptio form
class SubscriptioForm(ModelForm):
    student = ModelChoiceField(queryset=Student.objects.order_by('user'),widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Μαθητής',required=True)
    course = ModelChoiceField(queryset=Course.objects.order_by('title'),widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Course',required=True)
    user = ModelChoiceField(queryset=get_user_model().objects.order_by('last_name'),widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Καθηγητής',required=True)
    start_date = forms.DateField(initial=date.today,widget=forms.DateInput(attrs={'type': 'date','class': 'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-700 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6','placeholder': 'YYYY-MM-DD',}),required=True,label='Έναρξη')
    #end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-700 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6','placeholder': 'YYYY-MM-DD',}),required=False)
    is_online = forms.BooleanField(label='Κατάσταση', initial=True, required=False)
    
    class Meta:
        model = Subscription
        fields = ("user","student","course","start_date","is_online")

    def __init__(self, *args, **kwargs):
        super(SubscriptioForm, self).__init__(*args, **kwargs)
        self.fields['end_date'].disabled = True
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SubscriptioForm, self).__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                self.fields['student'].queryset = Student.objects.all()
                self.fields['course'].queryset = Course.objects.all()
            else:
                self.fields['student'].queryset = Student.objects.filter(user__organization=user.organization.id,is_student=True)
                self.fields['course'].queryset = Course.objects.filter(organization=user.organization.id)
                self.fields['user'].queryset = get_user_model().objects.filter(organization=user.organization.id,is_staff=True)


# Subscriptio Update form
class SubscriptionUpdateForm(ModelForm):
    student = ModelChoiceField(queryset=Student.objects.order_by('user'),widget=forms.Select(attrs={'class': 'form-control'}),label='Μαθητής')
    course = ModelChoiceField(queryset=Course.objects.order_by('title'),widget=forms.Select(attrs={'class': 'form-control'}),label='Course')
    user = ModelChoiceField(queryset=get_user_model().objects.order_by('last_name'),widget=forms.Select(attrs={'class': 'form-control'}),label='Καθηγητής')
    start_date = forms.DateField(initial=date.today,widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),label='Έναρξη')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),label='Λήξη',required=False)
    is_online = forms.BooleanField(label='Κατάσταση', initial=True, required=False)
    is_paid = forms.BooleanField(label='Ανανεώθηκε', initial=False, required=False)
    
    class Meta:
        model = Subscription
        fields = ("user","student","course","start_date","is_online",'is_paid')

    def __init__(self, *args, **kwargs):
        super(SubscriptionUpdateForm, self).__init__(*args, **kwargs)
        self.fields['end_date'].disabled = True
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SubscriptionUpdateForm, self).__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                self.fields['student'].queryset = Student.objects.all()
                self.fields['course'].queryset = Course.objects.all()
            else:
                self.fields['student'].queryset = Student.objects.filter(user__organization=user.organization.id,is_student=True)
                self.fields['course'].queryset = Course.objects.filter(organization=user.organization.id)


# Course form
class CourseForm(forms.ModelForm):
    organization = ModelChoiceField(queryset=Organization.objects.all(),widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),empty_label='---Επιλέξτε Οργανισμό---',label=False,required=True)
    title = forms.CharField(label=False, widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700','placeholder':'Μάθημα'}),required=True)
    description = forms.CharField(label=False, widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700','placeholder':'Περιγραφή'}),required=False)
    is_online = forms.BooleanField(initial=True,label='Κατάσταση',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    class Meta:
        model = Course
        fields = ['organization','title', 'description','is_online']
        widgets = {
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CourseForm, self).__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                # self.fields['member'].queryset = Member.objects.all()
                self.fields['organization'].queryset = Organization.objects.all()
            else:
                # self.fields['member'].queryset = Member.objects.filter(user__company=user.company.id,is_student=True)
                self.fields['organization'].queryset = Organization.objects.filter(user__organization=user.organization.id).distinct()


# Course update form
class CourseUpdateForm(forms.ModelForm):
    organization = ModelChoiceField(queryset=Organization.objects.all(),widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),empty_label='---Επιλέξτε Οργανισμό---',label=False,required=True)
    title = forms.CharField(label=False, widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700','placeholder':'Μάθημα'}),required=True)
    description = forms.CharField(label=False, widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700','placeholder':'Περιγραφή'}),required=False)
    is_online = forms.BooleanField(initial=True,label='Κατάσταση',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    class Meta:
        model = Course
        fields = ['organization','title', 'description','is_online']
        widgets = {
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CourseUpdateForm, self).__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                # self.fields['member'].queryset = Member.objects.all()
                self.fields['organization'].queryset = Organization.objects.all()
            else:
                # self.fields['member'].queryset = Member.objects.filter(user__company=user.company.id,is_student=True)
                self.fields['organization'].queryset = Organization.objects.filter(user__organization=user.organization.id).distinct()