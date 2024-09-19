from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import EmailAuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView,ListView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django_filters.views import FilterView
from .filters import UserStaffFillter
from .models import UserFile


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
            return render(request, 'app/users/login.html', {'form': form})
    else:
        form = EmailAuthenticationForm()
    return render(request, 'app/users/login.html', {'form': form})



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
    

    def get_queryset(self):
        queryset = super().get_queryset()
        if  self.request.user.is_superuser:
            queryset = get_user_model().objects.all()
        else:
            queryset = queryset.filter(is_staff=True,organization=self.request.user.organization)
        return queryset

from django.contrib import messages

# Staff Create View
class UserStaffCreateView(LoginRequiredMixin,CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = "app/staff/staff_new.html"
    success_url = reverse_lazy('staff_new')
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


    # def get_queryset(self):
    #     # Return only the courses associated with the current logged-in user
    #     return self.request.user.courses.all()
   
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        initial['is_staff'] = True  # Set the initial value as needed
        return initial

    def form_valid(self, form):
        # Retain the value of the disabled field
        form.cleaned_data['is_staff'] = self.get_initial()['is_staff']
        return super().form_valid(form)

    def form_valid(self, form):
        # Add a success message after a successful form submission
        messages.success(self.request, 'Your form has been submitted successfully!')
        return super().form_valid(form)

# Staff Update View
class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = get_user_model()
    #fields = '__all__'
    template_name = 'app/staff/staff_edit.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('home')
    



# Student - User create
# class StudentUserCreateView(LoginRequiredMixin,CreateView):
#     model = get_user_model()
#     form_class = UserCreationForm
#     template_name = "app/student/student_new.html"
#     success_url = reverse_lazy('home')
    
#     def form_invalid(self, form):
#         print(form.errors)
#         return super().form_invalid(form)
    
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
    
#     def get_initial(self):
#         initial = super().get_initial()
#         initial['is_student'] = True  # Set the initial value as needed
#         return initial
    
#     def form_valid(self, form):
#         form.cleaned_data['is_student'] = self.get_initial()['is_student']
#         return super().form_valid(form)


# Student - User Update
class StudentUserUpdateView(LoginRequiredMixin,UpdateView):
    model = get_user_model()
    #fields = '__all__'
    template_name = 'app/student/student_edit.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('home')

    # def form_valid(self, form):
    #     try:
    #         response = super().form_valid(form)
    #         logger.info(f'Member "{self.object}" updated successfully.')
    #         messages.success(self.request, 'Member updated successfully.')
    #         return response
    #     except Exception as e:
    #         logger.error(f'Error updating book: {e}')
    #         form.add_error(None, 'An error occurred while updating the member.')
    #         return super().form_invalid(form)





    # def form_valid(self, form):
    #     try:
    #         response = super().form_valid(form)
    #         logger.info(f'Member "{self.object}" updated successfully.')
    #         messages.success(self.request, 'Member updated successfully.')
    #         return response
    #     except Exception as e:
    #         logger.error(f'Error updating book: {e}')
    #         form.add_error(None, 'An error occurred while updating the member.')
    #         return super().form_invalid(form)



# File list
class DocumentListView(LoginRequiredMixin,ListView):
    model = get_user_model()
    template_name = 'app/files/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['row_count'] = UserFile.objects.count()  # Count the rows
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserFile.objects.all()  # Staff can see all articles
        else:
            return UserFile.objects.filter(user__student__is_student=True, user__is_staff=False,user__student__organization=self.request.user.organization)