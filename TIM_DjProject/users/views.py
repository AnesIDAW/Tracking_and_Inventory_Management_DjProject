from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# User Registration View (Clients)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('dashboard')  # Redirect to dashboard after registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/admin/' if user.role == 'admin' else 'client_dashboard')  # Redirect to Dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('/users/login/')

def custom_logout(request):
    logout(request)
    return redirect('/users/login/')

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')  # Placeholder template