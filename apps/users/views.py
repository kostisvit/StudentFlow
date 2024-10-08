from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import EmailAuthenticationForm, UserCreationForm, UserChangeForm, VacationStaffForm, MultipleUserFileForm, StaffMultipleUserFileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView,ListView, TemplateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,DeleteView
from django_filters.views import FilterView
from .filters import UserStaffFillter, DocumentFilter, VacationFilter
from .models import Document, Vacation, EmployeeDocument
from .password_change import *
from .export import Staff_export
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import User


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



# Staff List View
class UserStaffView(LoginRequiredMixin,FilterView):
    model = get_user_model()
    filterset_class = UserStaffFillter
    context_object_name = 'users'
    template_name = "app/staff/staff.html"

    # Pass the logged-in user to the form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the logged-in user to the form
        return kwargs
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
            return redirect('staff_list')  # Redirect to course list after submission
        return self.get(request, *args, form=form)

    def get_queryset(self):
        queryset = super().get_queryset()
        if  self.request.user.is_superuser:
            queryset = get_user_model().objects.filter(is_staff=True)
        else:
            queryset = queryset.filter(is_staff=True,organization=self.request.user.organization)
        return queryset


# Staff Update Function View
@login_required
def staff_update(request, pk):
    post = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('staff_list')
    else:
        form = UserChangeForm(instance=post)
    return render(request, 'app/staff/staff_edit.html', {'form': form})


# Upload File to User
@login_required
def student_upload_files(request):
    logged_in_user = request.user  # Get the logged-in user

    if request.method == 'POST':
        form = MultipleUserFileForm(request.POST, request.FILES, logged_in_user=logged_in_user)
        if form.is_valid():
            selected_user = form.cleaned_data['user']
            filename = form.cleaned_data['filename']
            course = form.cleaned_data['course']
            file = request.FILES.getlist('file')
            for file in file:
                Document.objects.create(user=selected_user, file=file,filename=filename,course=course)
            messages.success(request, 'Files uploaded successfully!')
            return redirect('student_upload_files')  # Redirect to a success page
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = MultipleUserFileForm(logged_in_user=logged_in_user)

    return render(request, 'app/files/student_document_upload.html', {'form': form})



# Upload File Staff
def staff_upload_files(request):
    logged_in_user = request.user  # Get the logged-in user

    if request.method == 'POST':
        form = StaffMultipleUserFileForm(request.POST, request.FILES, logged_in_user=logged_in_user)

        if form.is_valid():
            # Extract valid data
            selected_user = form.cleaned_data['user']
            filename = form.cleaned_data['filename']
            course = form.cleaned_data['course']
            files = form.cleaned_data['file']  # This will be the list of uploaded files

            # Iterate through files and create EmployeeDocument entries
            for file in files:
                EmployeeDocument.objects.create(user=selected_user, file=file, filename=filename, course=course)

            messages.success(request, 'Files uploaded successfully!')
            return redirect('staff_upload_files')  # Redirect after success
        else:
            # Log errors to the console
            print("Form Errors:", form.errors)
            messages.error(request, 'Please correct the errors below and try again.')

    else:
        form = StaffMultipleUserFileForm(logged_in_user=logged_in_user)

    return render(request, 'app/files/staff_document_upload.html', {'form': form})


# Document list
class DocumentListView(LoginRequiredMixin,FilterView):
    model = Document
    template_name = 'app/files/student_document_list.html'
    filterset_class = DocumentFilter
    context_object_name = 'documents'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['row_count'] = Document.objects.count()  # Count the rows
        return context
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Document.objects.all()  # Staff can see all articles
        else:
            return Document.objects.filter(user__student__is_student=True, user__is_staff=False,user__student__organization=self.request.user.organization)


# Document list
class StaffDocumentListView(LoginRequiredMixin,FilterView):
    model = EmployeeDocument
    template_name = 'app/files/staff_document_list.html'
    filterset_class = DocumentFilter
    context_object_name = 'documents'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['row_count'] = EmployeeDocument.objects.count()  # Count the rows
        return context
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EmployeeDocument.objects.all()  # Staff can see all articles
        else:
            return EmployeeDocument.objects.filter(user__organization=self.request.user.organization)



class VacationStaffListView(LoginRequiredMixin, FilterView):
    model = Vacation
    template_name = 'app/staff/staff_vacation_list.html'
    filterset_class = VacationFilter
    context_object_name = 'vacations'
    paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['vacations_empty'] = not context['vacations'].exists()
    #     return context

    # Override to add the form to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VacationStaffForm()  # Inject the form into the context
        return context

    # Handle form submission (manual post method for CreateView functionality)
    def post(self, request, *args, **kwargs):
        form = VacationStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vacations_list')  # Redirect to course list after submission
        return self.get(request, *args, form=form)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Vacation.objects.all()  # Staff can see all articles
        else:
            return Vacation.objects.filter(user__organization=self.request.user.organization)


class UserFileDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = User
    template_name = 'app/staff/staff_delete_confirm.html'
    success_url = reverse_lazy('home') 
    
    def test_func(self):
        return self.request.user.is_company_owner or self.request.user.is_superuser


    
    