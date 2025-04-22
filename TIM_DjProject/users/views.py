from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test
from inventory.models import Product

# User Registration View (Clients)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Clients')
            user.groups.add(group)
            login(request, user)  # Auto-login after registration
            return redirect('dashboard:client_dashboard')  # Redirect to dashboard after registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def is_staff_user(user):
    return user.is_authenticated and user.is_staff

# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            print("User Groups:", list(user.groups.values_list('name', flat=True)))
            login(request, user)

            if user.is_superuser or is_staff_user(user):
                return redirect('dashboard:admin_dashboard')
            else:
                return redirect('dashboard:client_dashboard')
        else:
            print("Form Errors:", form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

