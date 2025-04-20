from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from django.urls import reverse

# User Registration View (Clients)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Clients')
            user.groups.add(group)
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
            print("User Groups:", list(user.groups.values_list('name', flat=True)))
            login(request, user)

            if user.groups.filter(name='Staff').exists():
                return redirect('dashboard:admin_dashboard')
            else:
                return redirect('dashboard:client_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


# User Logout View
def user_logout(request):
    logout(request)
    return redirect('/users/login/')

"""def custom_logout(request):
    logout(request)
    return redirect('/users/login/')"""