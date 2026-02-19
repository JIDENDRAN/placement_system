from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, RoleLoginForm
from .models import User
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
        from companies.models import Company
        from django.utils import timezone
        from django.db.models.functions import ExtractMonth
        from django.db.models import Count
        import calendar

        total_students = User.objects.filter(role='STUDENT').count()
        total_alumni = User.objects.filter(role='ALUMNI').count()
        active_companies = Company.objects.filter(active_hiring=True).count()
        
        now = timezone.now()
        drives_this_month = Company.objects.filter(
            recruitment_drive_date__year=now.year,
            recruitment_drive_date__month=now.month
        ).count()
        
        # Chart Data: Student registrations over last 6 months
        last_6_months = []
        chart_labels = []
        chart_data = []
        
        for i in range(5, -1, -1):
            month_date = now - timezone.timedelta(days=i*30)
            month_name = calendar.month_name[month_date.month][:3]
            count = User.objects.filter(
                role='STUDENT',
                date_joined__year=month_date.year,
                date_joined__month=month_date.month
            ).count()
            chart_labels.append(month_name)
            chart_data.append(count)

        context = {
            'total_students': total_students,
            'total_alumni': total_alumni,
            'active_companies': active_companies,
            'drives_this_month': drives_this_month,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
        }
        return render(request, 'accounts/admin_dashboard.html', context)
    elif user.role == 'ALUMNI':
        from feedback.models import InterviewFeedback
        feedbacks = InterviewFeedback.objects.filter(alumni=user).order_by('-created_at')
        shared_companies = feedbacks.values_list('company__name', flat=True).distinct()
        context = {
            'feedbacks_count': feedbacks.count(),
            'latest_feedbacks': feedbacks[:5],
            'shared_companies': shared_companies,
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

@login_required
def user_list_view(request):
    if request.user.role != 'ADMIN':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')
    query = request.GET.get('q')
    if query:
        users = users.filter(username__icontains=query) | users.filter(email__icontains=query)
        
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
def toggle_user_status_view(request, user_id):
    if request.user.role != 'ADMIN':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    user_to_toggle = get_object_or_404(User, id=user_id)
    if user_to_toggle.is_superuser:
        messages.error(request, "Cannot modify superuser status.")
    else:
        user_to_toggle.is_active = not user_to_toggle.is_active
        user_to_toggle.save()
        status = "activated" if user_to_toggle.is_active else "blocked"
        messages.success(request, f"User {user_to_toggle.username} has been {status}.")
    
    return redirect('user_list')

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'home.html')
