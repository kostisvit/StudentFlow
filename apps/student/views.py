from django.shortcuts import render
from .models import Student
from .filters import StudentFilter, SubscriptionFilter
from django_filters.views import FilterView
from django.views.generic import CreateView, UpdateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from .forms import *
from .export import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from .forms import CourseForm 
from .send_email_view import compose_email
from django.shortcuts import get_object_or_404


UserModel = get_user_model()

#fake view for testing
from django.http import HttpResponse, JsonResponse
def fake_view(request):
    return HttpResponse("This is a fake view for testing purposes.")

# Student list view
class StudentListView(LoginRequiredMixin,FilterView):
    model = Student
    template_name = 'app/student/student_list.html'
    context_object_name = 'students'
    filterset_class = StudentFilter
    paginate_by = 10
    
    def get_filterset_kwargs(self, filterset_class):
        # Get the default kwargs from the parent method
        kwargs = super().get_filterset_kwargs(filterset_class)
        # Add the current user to the kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    # Override to add the form to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StudentCreationForm()  # Inject the form into the context
        return context

    # Handle form submission (manual post method for CreateView functionality)
    def post(self, request, *args, **kwargs):
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students_list')  # Redirect to course list after submission
        return self.get(request, *args, form=form)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            # Apply filter for superuser
            queryset = queryset.filter(is_student=True)  # Replace with your actual filter conditions for superusers
        else:
            # Apply different filter for regular users
            queryset = queryset.filter(user__organization=self.request.user.organization, is_student=True)  # Replace with your actual filter conditions for regular users
        return queryset


from django.contrib import messages
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
        """Override to handle the selected course and assign it to the user."""
        user = form.save(commit=False)
        course = form.cleaned_data.get('course_title')
        user.save()
    
    def form_valid(self, form):
        form.cleaned_data['is_student'] = self.get_initial()['is_student']
        return super().form_valid(form)

    def form_valid(self, form):
        # Add a success message after a successful form submission
        messages.success(self.request, 'Your form has been submitted successfully!')
        return super().form_valid(form)


# Student update view
class StudentUserUpdateView(LoginRequiredMixin,UpdateView):
    model = Student
    #fields = '__all__'
    template_name = 'app/student/student_edit.html'
    form_class = StudentUserChangeForm
    success_url = reverse_lazy('home')

    # def form_invalid(self, form):
    #     print(form.errors)
    #     return super().form_invalid(form)
    
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs
    
    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['is_student'] = True  # Set the initial value as needed
    #     return initial

    # def form_valid(self, form):
    #     """Override to handle the selected course and assign it to the user."""
    #     user = form.save(commit=False)
    #     course = form.cleaned_data.get('course_title')
    #     user.save()
    
    # def form_valid(self, form):
    #     form.cleaned_data['is_student'] = self.get_initial()['is_student']
    #     return super().form_valid(form)

    # def form_valid(self, form):
    #     # Add a success message after a successful form submission
    #     messages.success(self.request, 'Your form has been changed successfully!')
    #     return super().form_valid(form)


    
# Subscription list 
class SubscriptionListView(LoginRequiredMixin, FilterView):
    model = Subscription
    #fields = '__all__'
    filterset_class = SubscriptionFilter
    template_name = 'app/student/subscriptions_list.html'
    context_object_name = 'subscriptions'
    paginate_by = 10
    
    def get_filterset_kwargs(self, filterset_class):
        # Get the default kwargs from the parent method
        kwargs = super().get_filterset_kwargs(filterset_class)
        # Add the current user to the kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    # Override to add the form to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubscriptionForm()  # Inject the form into the context
        return context

    # Handle form submission (manual post method for CreateView functionality)
    def post(self, request, *args, **kwargs):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscriptions_list')  # Redirect to course list after submission
        return self.get(request, *args, form=form)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            # Apply filter for superuser
            queryset = Subscription.objects.all()  # Replace with your actual filter conditions for superusers
        else:
            # Apply different filter for regular users
            queryset = queryset.filter(student__user__organization=self.request.user.organization)  # Replace with your actual filter conditions for regular users
        return queryset.order_by('-end_date')






# Subscriptions ending date list
class SubscriptionEndsListView(LoginRequiredMixin, FilterView):
    model = Subscription
    filterset_class = SubscriptionFilter
    template_name = 'app/student/subscription_ends_list.html'
    context_object_name = 'subscriptions'
    paginate_by = 10


    def get_filterset_kwargs(self, filterset_class):
        # Get the default kwargs from the parent method
        kwargs = super().get_filterset_kwargs(filterset_class)
        # Add the current user to the kwargs
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_queryset(self):
        # Get today's date
        today = timezone.now().date()
        # Calculate the date 5 days from now
        cutoff_date = today + timedelta(days=15)
        # Filter queryset where end_date is less than or equal to the cutoff date
        queryset = super().get_queryset().filter(end_date__lte=cutoff_date)
        return queryset



    
# Course LIst with modal creating new course
class CourseListView(LoginRequiredMixin,ListView):
    model = Course
    template_name = 'app/student/student_course_list.html'
    context_object_name = 'courses'
     
    # Override to add the form to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CourseForm()  # Inject the form into the context
        return context


    # Handle form submission (manual post method for CreateView functionality)
    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect to course list after submission
        return self.get(request, *args, form=form)




# Course update
class CourseUpdateView(LoginRequiredMixin,UpdateView):
    model = Course
    form_class = CourseUpdateForm
    template_name = 'app/student/student_course_update.html'  # This will be rendered in the modal
    success_url = reverse_lazy('course_list')  # Redirect after successful update

    def get_object(self, queryset=None):
        # Ensure you retrieve the object based on the primary key from the URL or modal
        obj = get_object_or_404(Course, pk=self.kwargs['pk'])
        return obj