from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import MockInterview, MockInterviewFeedback
from accounts.models import User

class InterviewListView(LoginRequiredMixin, ListView):
    model = MockInterview
    template_name = 'mock_interviews/interview_list.html'
    context_object_name = 'interviews'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return MockInterview.objects.all().order_by('-scheduled_at')
        elif user.role == 'ALUMNI':
            return MockInterview.objects.filter(interviewer=user).order_by('-scheduled_at')
        else:
            return MockInterview.objects.filter(student=user).order_by('-scheduled_at')

from .forms import MockInterviewForm

class ScheduleInterviewView(LoginRequiredMixin, CreateView):
    model = MockInterview
    form_class = MockInterviewForm
    template_name = 'mock_interviews/schedule_interview.html'
    success_url = reverse_lazy('interview_list')

    def form_valid(self, form):
        messages.success(self.request, "Mock Interview scheduled successfully!")
        return super().form_valid(form)

@login_required
def interview_detail(request, pk):
    interview = get_object_or_404(MockInterview, pk=pk)
    feedback = getattr(interview, 'feedback', None)
    
    # Check permission
    if request.user != interview.student and request.user != interview.interviewer and request.user.role != 'ADMIN':
        messages.error(request, "You don't have permission to view this interview.")
        return redirect('interview_list')
        
    return render(request, 'mock_interviews/interview_detail.html', {
        'interview': interview,
        'feedback': feedback
    })

@login_required
def submit_feedback(request, pk):
    interview = get_object_or_404(MockInterview, pk=pk)
    
    # Only interviewer or admin can submit feedback
    if request.user != interview.interviewer and request.user.role != 'ADMIN':
        messages.error(request, "Only the assigned interviewer can submit feedback.")
        return redirect('interview_detail', pk=pk)

    if request.method == 'POST':
        try:
            form_data = {
                'technical_score': int(request.POST.get('technical_score', 0)),
                'communication_score': int(request.POST.get('communication_score', 0)),
                'behavioral_score': int(request.POST.get('behavioral_score', 0)),
                'problem_solving_score': int(request.POST.get('problem_solving_score', 0)),
                'strengths': request.POST.get('strengths', ''),
                'areas_of_improvement': request.POST.get('areas_of_improvement', ''),
                'overall_comments': request.POST.get('overall_comments', ''),
                'is_ready_for_real_interview': request.POST.get('is_ready') == 'on'
            }
            
            MockInterviewFeedback.objects.update_or_create(
                interview=interview,
                defaults=form_data
            )
            
            interview.status = 'COMPLETED'
            interview.save()
            
            messages.success(request, "Feedback submitted successfully!")
            return redirect('interview_detail', pk=pk)
        except ValueError:
            messages.error(request, "Please enter valid numbers for the scores.")
            return redirect('submit_feedback', pk=pk)

    return render(request, 'mock_interviews/submit_feedback.html', {'interview': interview})
