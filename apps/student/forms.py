from django import forms
from datetime import date
from django.forms import ModelForm,ModelChoiceField
from .models import Subscription, Course, Student
from organization.models import Organization
from users.models import User



class SubscriptioForm(ModelForm):
    student = ModelChoiceField(queryset=Student.objects.order_by('user'),widget=forms.Select(attrs={'class': 'form-control'}),label='Μαθητής')
    course = ModelChoiceField(queryset=Course.objects.order_by('title'),widget=forms.Select(attrs={'class': 'form-control'}),label='Course')
    user = ModelChoiceField(queryset=User.objects.order_by('last_name'),widget=forms.Select(attrs={'class': 'form-control'}),label='Καθηγητής')
    start_date = forms.DateField(initial=date.today,widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),label='Έναρξη')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),label='Λήξη',required=False)
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
                self.fields['user'].queryset = User.objects.filter(organization=user.organization.id,is_staff=True)



class SubscriptionUpdateForm(ModelForm):
    student = ModelChoiceField(queryset=Student.objects.order_by('user'),widget=forms.Select(attrs={'class': 'form-control'}),label='Μαθητής')
    course = ModelChoiceField(queryset=Course.objects.order_by('title'),widget=forms.Select(attrs={'class': 'form-control'}),label='Course')
    user = ModelChoiceField(queryset=User.objects.order_by('last_name'),widget=forms.Select(attrs={'class': 'form-control'}),label='Καθηγητής')
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



class CourceForm(forms.ModelForm):
    organization = ModelChoiceField(queryset=Organization.objects.order_by('title'),widget=forms.Select(attrs={'class': 'form-control'}),label='Εταιρεία')
    
    class Meta:
        model = Course
        fields = ['organization','title', 'description','is_online']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Τίτλος',
                'maxlength': '50',
                'size': '20',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Περιγραφή',
                'maxlength': '50',
                'size': '100',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CourceForm, self).__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                # self.fields['member'].queryset = Member.objects.all()
                self.fields['organization'].queryset = Organization.objects.all()
            else:
                # self.fields['member'].queryset = Member.objects.filter(user__company=user.company.id,is_student=True)
                self.fields['organization'].queryset = Organization.objects.filter(user__organization=user.organization.id).distinct()