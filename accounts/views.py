from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    if user.role == 'ADMIN':
        return render(request, 'accounts/admin_dashboard.html')
    elif user.role == 'ALUMNI':
        return render(request, 'accounts/alumni_dashboard.html')
    else:
        return render(request, 'accounts/student_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'home.html')
