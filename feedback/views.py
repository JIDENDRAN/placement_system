from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import InterviewFeedback, InterviewRound
from companies.models import Company
from django.urls import reverse_lazy

class FeedbackListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = InterviewFeedback
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 10

    def test_func(self):
        return self.request.user.role in ['ADMIN', 'ALUMNI', 'STUDENT']

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return InterviewFeedback.objects.filter(company__name__icontains=query)
        return InterviewFeedback.objects.all().order_by('-created_at')

class FeedbackDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = InterviewFeedback
    template_name = 'feedback/feedback_detail.html'

    def test_func(self):
        return self.request.user.role in ['ADMIN', 'ALUMNI', 'STUDENT']

class FeedbackCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = InterviewFeedback
    fields = ['company', 'job_role', 'salary_package', 'interview_date', 'rounds_count', 'core_technical_topics', 'placement_type', 'interview_type', 'overall_experience', 'overall_difficulty', 'status', 'tips', 'culture_fit_advice']
    template_name = 'feedback/feedback_form.html'
    success_url = reverse_lazy('feedback_list')

    def test_func(self):
        return self.request.user.role in ['ALUMNI', 'ADMIN']

    def form_valid(self, form):
        form.instance.alumni = self.request.user
        return super().form_valid(form)
