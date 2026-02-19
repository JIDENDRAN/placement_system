from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import InterviewFeedback, InterviewRound
from companies.models import Company
from django.urls import reverse_lazy
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import io

class FeedbackListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = InterviewFeedback
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 10

    def test_func(self):
        return self.request.user.role in ['ADMIN', 'ALUMNI', 'STUDENT']

    def get_queryset(self):
        queryset = InterviewFeedback.objects.all().order_by('-created_at')
        query = self.request.GET.get('q')
        company_id = self.request.GET.get('company')
        
        if query:
            queryset = queryset.filter(company__name__icontains=query) | queryset.filter(job_role__icontains=query)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        selected_company = self.request.GET.get('company')
        context['selected_company'] = int(selected_company) if selected_company and selected_company.isdigit() else None
        return context

class FeedbackDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = InterviewFeedback
    template_name = 'feedback/feedback_detail.html'
    context_object_name = 'feedback'

    def test_func(self):
        return self.request.user.role in ['ADMIN', 'ALUMNI', 'STUDENT']

class FeedbackCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = InterviewFeedback
    fields = ['company', 'job_role', 'salary_package', 'interview_date', 'rounds_count', 'core_technical_topics', 'placement_type', 'interview_type', 'overall_experience', 'overall_difficulty', 'status', 'tips', 'culture_fit_advice']
    template_name = 'feedback/feedback_form.html'
    success_url = reverse_lazy('feedback_list')

    def test_func(self):
        return self.request.user.role in ['ALUMNI', 'ADMIN', 'STUDENT']

    def form_valid(self, form):
        form.instance.alumni = self.request.user
        return super().form_valid(form)

@login_required
def export_feedback_pdf(request):
    if request.user.role != 'ADMIN':
        return HttpResponse("Unauthorized", status=401)
    
    company_id = request.GET.get('company')
    feedbacks = InterviewFeedback.objects.all().order_by('-created_at')
    
    title = "Complete Placement Feedback Report"
    if company_id:
        company = get_object_or_404(Company, id=company_id)
        feedbacks = feedbacks.filter(company=company)
        title = f"Feedback Report for {company.name}"

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 12))

    if not feedbacks.exists():
        elements.append(Paragraph("No feedback reports found for the selected criteria.", styles['Normal']))
    else:
        for fb in feedbacks:
            elements.append(Paragraph(f"<b>Company:</b> {fb.company.name}", styles['Normal']))
            elements.append(Paragraph(f"<b>Role:</b> {fb.job_role}", styles['Normal']))
            elements.append(Paragraph(f"<b>Package:</b> {fb.salary_package or 'N/A'}", styles['Normal']))
            alumni_name = fb.alumni.get_full_name() or fb.alumni.username
            elements.append(Paragraph(f"<b>Shared by:</b> {alumni_name} ({fb.alumni.get_role_display()})", styles['Normal']))
            elements.append(Paragraph(f"<b>Date:</b> {fb.interview_date}", styles['Normal']))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph("<b>Experience:</b>", styles['Normal']))
            elements.append(Paragraph(fb.overall_experience, styles['Normal']))
            elements.append(Spacer(1, 12))
            elements.append(Paragraph("-" * 100, styles['Normal']))
            elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"placement_reports_{timezone.now().strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
