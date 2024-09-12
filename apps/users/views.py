from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import EmailAuthenticationForm
from django.contrib.auth import authenticate, login


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
