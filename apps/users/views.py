from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import EmailAuthenticationForm, UserCreationForm, UserChangeForm, VacationStaffForm, StudentFileForm, StaffFileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django_filters.views import FilterView
from .filters import UserStaffFillter, DocumentFilter, VacationFilter
from .models import Document, Vacation, EmployeeDocument
from .password_change import *
from .export import Staff_export
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import User
from django.core.paginator import Paginator


UserModel = get_user_model()

#fake view for testing
from django.http import HttpResponse
def fake_view(request):
    return HttpResponse("This is a fake view for testing purposes.")

# Login user function
def custom_login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
        else:
            # If the form is invalid, the error message will be shown on the form
            return render(request, 'app/accounts/login.html', {'form': form})
    else:
        form = EmailAuthenticationForm()
    return render(request, 'app/accounts/login.html', {'form': form})



# Logout user function
def custom_logout(request):
    logout(request)
    return redirect('login')

#########################################################################################################



# Staff List View
class UserStaffView(LoginRequiredMixin,FilterView):
    model = get_user_model()
    filterset_class = UserStaffFillter
    context_object_name = 'users'
    template_name = "app/staff/staff.html"
    paginate_by = 10

    # Pass the logged-in user to the form
    def get_context_data(self, **kwargs):
        # Get the base context from the base implementation
        context = super().get_context_data(**kwargs)
        # Add the logged-in user to the context
        context['logged_in_user'] = self.request.user
        return context
    
    # Override to add the form to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserCreationForm()  # Inject the form into the context
        return context

    # Handle form submission (manual post method for CreateView functionality)
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')  
        return self.get(request, *args, form=form)

    def get_queryset(self):
        queryset = super().get_queryset()
        if  self.request.user.is_superuser:
            queryset = get_user_model().objects.filter(is_staff=True)
        else:
            queryset = queryset.filter(is_staff=True,organization=self.request.user.organization)
        return queryset

#########################################################################################################


# Staff Update Function View
@login_required
def staff_update(request, pk):
    # Retrieve the user object to be updated
    post = get_object_or_404(User, pk=pk)

    # Check if the requesting user is a company owner or superuser
    if not (request.user.is_company_owner or request.user.is_superuser):
        return render(request, '403.html', status=403)

    # Handle form submission
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('staff_list')
    else:
        form = UserChangeForm(instance=post)

    # Render the edit form
    return render(request, 'app/staff/staff_edit.html', {'form': form})

#########################################################################################################

# Upload File User
@login_required
def student_upload_files(request):
    logged_in_user = request.user  

    if request.method == 'POST':
        form = StudentFileForm(request.POST, request.FILES, logged_in_user=logged_in_user)
        if form.is_valid():
            selected_user = form.cleaned_data['user']
            filename = form.cleaned_data['filename']
            course = form.cleaned_data['course']
            file = request.FILES.getlist('file')
            for file in file:
                Document.objects.create(user=selected_user, file=file,filename=filename,course=course)
            messages.success(request, 'Files uploaded successfully!')
            return redirect('student_upload_files')  
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = StudentFileForm(logged_in_user=logged_in_user)

    return render(request, 'app/files/student_document_upload.html', {'form': form})

#########################################################################################################

# Upload File Staff
def staff_upload_files(request):
    logged_in_user = request.user  

    if request.method == 'POST':
        form = StaffFileForm(request.POST, request.FILES, logged_in_user=logged_in_user)

        if form.is_valid():
            # Extract valid data
            selected_user = form.cleaned_data['user']
            filename = form.cleaned_data['filename']
            course = form.cleaned_data['course']
            files = form.cleaned_data['file']  

            # Iterate through files and create EmployeeDocument entries
            for file in files:
                EmployeeDocument.objects.create(user=selected_user, file=file, filename=filename, course=course)

            messages.success(request, 'Files uploaded successfully!')
            return redirect('staff_upload_files')  
        else:
            # Log errors to the console
            print("Form Errors:", form.errors)
            messages.error(request, 'Please correct the errors below and try again.')

    else:
        form = StaffFileForm(logged_in_user=logged_in_user)

    return render(request, 'app/files/staff_document_upload.html', {'form': form})

#########################################################################################################


# Document list
class StudentDocumentListView(LoginRequiredMixin,FilterView):
    model = Document
    template_name = 'app/files/student_document_list.html'
    filterset_class = DocumentFilter
    context_object_name = 'documents'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['row_count'] = Document.objects.count()  
        return context
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Document.objects.all()  
        else:
            return Document.objects.filter(user__student__is_student=True, user__is_staff=False,user__student__organization=self.request.user.organization)

#########################################################################################################

# Staff Document list
class StaffDocumentListView(LoginRequiredMixin,FilterView):
    model = EmployeeDocument
    template_name = 'app/files/staff_document_list.html'
    filterset_class = DocumentFilter
    context_object_name = 'documents'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['row_count_superuser'] = EmployeeDocument.objects.all().count()  
            return context
        else:
            context['row_count'] = EmployeeDocument.objects.filter(user__organization=self.request.user.organization).count()  
            return context
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EmployeeDocument.objects.all() 
        else:
            return EmployeeDocument.objects.filter(user__organization=self.request.user.organization)

#########################################################################################################

# Staff Vacation List
@login_required
def vacation_staff_list_view(request):
    # Get the current user
    user = request.user

    # Filter queryset based on the user type
    if user.is_superuser:
        vacations = Vacation.objects.all()
    else:
        vacations = Vacation.objects.filter(user__organization=user.organization)

    # Apply filtering from VacationFilter
    filterset = VacationFilter(request.GET, queryset=vacations,user=request.user)
    filtered_vacations = filterset.qs

    # Paginate the results
    paginator = Paginator(filtered_vacations, 10)  # 10 vacations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle form submission for new vacation (POST request)
    if request.method == 'POST':
        form = VacationStaffForm(request.POST,user=request.user)
        if form.is_valid():
            form.save()
            return redirect('vacations_list')  # Redirect after saving the form
    else:
        form = VacationStaffForm(user=request.user)

    # Context to be passed to the template
    context = {
        'vacations': page_obj,
        'form': form,
        'filter': filterset
    }

    return render(request, 'app/staff/staff_vacation_list.html', context)

#########################################################################################################


# Staff dele
# class StaffDeleteView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
#     model = User
#     fields = ['is_active'] 
#     template_name = 'app/staff/staff_disable_confirm.html'
#     success_url = reverse_lazy('staff_list') 

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
#         return super().form_valid(form)

#     def get_object(self):
#         user_id = self.kwargs.get('pk')
#         return get_object_or_404(User, id=user_id)
    
#     def test_func(self):
#         return self.request.user.is_company_owner or self.request.user.is_superuser

#########################################################################################################

# Staff Document Delete
class StaffDocumentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = EmployeeDocument
    template_name = 'app/files/staff_document_confirm_delete.html'
    success_url = reverse_lazy('home') 
    
    def test_func(self):
        return self.request.user.is_company_owner or self.request.user.is_superuser
    
#########################################################################################################

# Student Document Delete
class StudentDocumentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Document
    template_name = 'app/files/student_document_confirm_delete.html'
    success_url = reverse_lazy('home') 
    
    def test_func(self):
        return self.request.user.is_company_owner or self.request.user.is_superuser
    
#########################################################################################################