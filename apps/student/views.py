from django.shortcuts import render
from .models import Student
from .filters import StudentFilter, SubscriptionFilter
from django_filters.views import FilterView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from .forms import *
from django.urls import reverse_lazy

UserModel = get_user_model()

# Member list view
class StudentListView(LoginRequiredMixin,FilterView):
    model = Student
    template_name = 'app/student/student.html'
    context_object_name = 'students'
    filterset_class = StudentFilter
    paginate_by = 10
    
    def get_filterset_kwargs(self, filterset_class):
        # Get the default kwargs from the parent method
        kwargs = super().get_filterset_kwargs(filterset_class)
        # Add the current user to the kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a flag indicating if the students list is empty
        context['students_empty'] = not context['students'].exists()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            # Apply filter for superuser
            queryset = queryset.filter(is_student=True)  # Replace with your actual filter conditions for superusers
        else:
            # Apply different filter for regular users
            queryset = queryset.filter(user__organization=self.request.user.organization, is_student=True)  # Replace with your actual filter conditions for regular users
        return queryset



# Student - User create
class StudentUserCreateView(LoginRequiredMixin,CreateView):
    model = get_user_model()
    form_class = StudentCreationForm
    template_name = "app/student/student_new.html"
    success_url = reverse_lazy('home')
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        initial['is_student'] = True  # Set the initial value as needed
        return initial
    
    def form_valid(self, form):
        form.cleaned_data['is_student'] = self.get_initial()['is_student']
        return super().form_valid(form)



# Subscription list 
class SubscriptionListView(LoginRequiredMixin, FilterView):
    model = Subscription
    #fields = '__all__'
    filterset_class = SubscriptionFilter
    template_name = 'app/student/subscriptions.html'
    context_object_name = 'subscriptions'
    paginate_by = 10
    
    def get_filterset_kwargs(self, filterset_class):
        # Get the default kwargs from the parent method
        kwargs = super().get_filterset_kwargs(filterset_class)
        # Add the current user to the kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a flag indicating if the members list is empty
        context['subscriptions_empty'] = not context['subscriptions'].exists()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            # Apply filter for superuser
            queryset = Subscription.objects.all()  # Replace with your actual filter conditions for superusers
        else:
            # Apply different filter for regular users
            queryset = queryset.filter(student__user__organization=self.request.user.organization)  # Replace with your actual filter conditions for regular users
        return queryset.order_by('-end_date')