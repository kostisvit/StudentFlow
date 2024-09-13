from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import EmailAuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


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


# Student User create
class StudentUserCreateView(LoginRequiredMixin,CreateView):
    model = UserModel
    form_class = UserCreationForm
    template_name = "app/student/student_new.html"
    success_url = reverse_lazy('home')
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        initial['is_student'] = True  # Set the initial value as needed
        return initial
    
    def form_valid(self, form):
        form.cleaned_data['is_student'] = self.get_initial()['is_student']
        return super().form_valid(form)