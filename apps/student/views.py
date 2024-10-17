from django.shortcuts import render
from .models import Student
from .filters import StudentFilter, SubscriptionFilter, CourseFilter
from django_filters.views import FilterView
from django.views.generic import CreateView, UpdateView,ListView
from django.views.generic.edit import UpdateView,DeleteView
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
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib import messages
from student.services.renew_subscription import renew_subscription
from django.core.exceptions import PermissionDenied

UserModel = get_user_model()

#fake view for testing
from django.http import HttpResponse, JsonResponse
def fake_view(request):
    return HttpResponse("This is a fake view for testing purposes.")

#########################################################################################################

# Student list view
class StudentListView(LoginRequiredMixin,FilterView):
    model = Student
    template_name = 'app/student/student_list.html'
    context_object_name = 'students'
    filterset_class = StudentFilter
    paginate_by = 10

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['user'] = self.request.user
        return kwargs
    
    # Override to add the form to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StudentCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students_list')
        return self.get(request, *args, form=form)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            queryset = queryset.filter(is_student=True)
        else:
            queryset = queryset.filter(user__organization=self.request.user.organization, is_student=True)
        return queryset

#########################################################################################################


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
        initial['is_student'] = True
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
        messages.success(self.request, 'Your form has been submitted successfully!')
        return super().form_valid(form)

#########################################################################################################

# Student update view
class StudentUserUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Student
    template_name = 'app/student/student_edit.html'
    form_class = StudentUserChangeForm
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_company_owner or self.request.user.is_superuser
    
    def get_initial(self):
        initial = super().get_initial()
        initial['is_student'] = True
        return initial

    def form_valid(self, form):
        """Override to handle the selected course and assign it to the user."""
        user = form.save(commit=False)
        course = form.cleaned_data.get('course_title')
        user.save()
    
    def form_valid(self, form):
        form.cleaned_data['is_student'] = self.get_initial()['is_student']
        return super().form_valid(form)

#########################################################################################################
 
# Subscription list 
@login_required
def subscription_list_view(request):
    if request.user.is_superuser:
        queryset = Subscription.objects.all()
    elif hasattr(request.user, 'organization'):
        queryset = Subscription.objects.filter(student__user__organization=request.user.organization)
    else:
        queryset = Subscription.objects.none()

    filterset = SubscriptionFilter(request.GET, queryset=queryset,user=request.user)
    filtered_queryset = filterset.qs

    paginator = Paginator(filtered_queryset.order_by('-end_date'), 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('subscriptions_list')  
    else:
        form = SubscriptionForm(user=request.user)

    context = {
        'page_obj': page_obj,
        'form': form,
        'filter': filterset
    }

    return render(request, 'app/student/subscriptions_list.html', context)


#########################################################################################################

# Subscriptions ending date list
class SubscriptionEndsListView(LoginRequiredMixin, FilterView):
    model = Subscription
    filterset_class = SubscriptionFilter
    template_name = 'app/student/subscription_ends_list.html'
    context_object_name = 'subscriptions'
    paginate_by = 10


    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_queryset(self):
        today = timezone.now().date()
        cutoff_date = today + timedelta(days=15)
        queryset = super().get_queryset().filter(end_date__lte=cutoff_date)
        return queryset


#########################################################################################################

@login_required
def subscription_update_view(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)

    if not (request.user.is_company_owner or request.user.is_superuser):
        raise PermissionDenied("You are not allowed to edit this subscription.")


    if request.method == 'POST':
        form = SubscriptionUpdateForm(request.POST, instance=subscription)
        
        if form.is_valid():
            subscription = form.save()
            if subscription.is_paid:
                new_subscription = renew_subscription(subscription)
            return redirect(reverse_lazy('subscriptions_list'))

    else:
        form = SubscriptionUpdateForm(instance=subscription)

    return render(request, 'app/student/subscription_edit.html', {'form': form})


#########################################################################################################

# class SubscriptionDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
#     model = Subscription
#     template_name = 'app/student/subscription_delete_confirm.html'
#     success_url = reverse_lazy('subscriptions_list') 
    
#     def test_func(self):
#         return self.request.user.is_company_owner or self.request.user.is_superuser


#########################################################################################################

# Course List with modal creating new course
def course_list_view(request):
    form = CourseForm(user=request.user)

    if request.user.is_superuser:
        queryset = Course.objects.all()
    else:
        queryset = Course.objects.filter(user__organization=request.user.organization)

    filterset = CourseFilter(request.GET, queryset=queryset,user=request.user)
    filtered_queryset = filterset.qs

    paginator = Paginator(filtered_queryset.order_by('-title'), 10)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = CourseForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('course_list')

    context = {
        'page_obj': page_obj,
        'form': form,
        'filter': filterset,
    }

    return render(request, 'app/student/student_course_list.html', context)

#########################################################################################################

# Course update
class CourseUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Course
    form_class = CourseUpdateForm
    template_name = 'app/student/student_course_update.html'
    success_url = reverse_lazy('course_list')

    def get_object(self, queryset=None):
        obj = get_object_or_404(Course, pk=self.kwargs['pk'])
        return obj

    def test_func(self):
        return self.request.user.is_company_owner or self.request.user.is_superuser

#########################################################################################################

# Delete View
# class StudentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
#     model = Student
#     template_name = 'app/student/student_confirm_delete.html'
#     success_url = reverse_lazy('home') 
    
#     def test_func(self):
#         return self.request.user.is_company_owner or self.request.user.is_superuser


