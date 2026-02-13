from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, RoleLoginForm
from django.contrib import messages

class CustomLoginView(LoginView):
    form_class = RoleLoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        selected_role = form.cleaned_data.get('role')
        if user.role != selected_role:
            messages.error(self.request, f"Access denied. You are registered as {user.role}, not {selected_role}.")
            return self.form_invalid(form)
        return super().form_valid(form)

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
        from feedback.models import InterviewFeedback
        feedbacks = InterviewFeedback.objects.filter(alumni=user).order_by('-created_at')
        context = {
            'feedbacks_count': feedbacks.count(),
            'latest_feedbacks': feedbacks[:5],
        }
        return render(request, 'accounts/alumni_dashboard.html', context)
    else:
        from mock_tests.models import StudentAttempt
        from companies.models import Company
        from django.db.models import Avg, F
        
        attempts = StudentAttempt.objects.filter(student=user).order_by('completed_at')
        tests_taken = attempts.count()
        
        # Calculate Average Score Percentage
        if tests_taken > 0:
            total_perc = sum([(a.score / a.total_marks) * 100 for a in attempts if a.total_marks > 0])
            avg_readiness = round(total_perc / tests_taken, 1)
        else:
            avg_readiness = 0
            
        active_drives = Company.objects.filter(active_hiring=True).count()
        
        # Data for chart
        chart_labels = [a.completed_at.strftime('%d %b') for a in attempts]
        chart_data = [round((a.score / a.total_marks) * 100, 1) if a.total_marks > 0 else 0 for a in attempts]
        
        # Get latest 5 attempts for dashboard table or summary
        latest_attempts = attempts.order_by('-completed_at')[:5]

        context = {
            'tests_taken': tests_taken,
            'avg_readiness': avg_readiness,
            'active_drives': active_drives,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
            'latest_attempts': latest_attempts,
        }
        return render(request, 'accounts/student_dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'home.html')
