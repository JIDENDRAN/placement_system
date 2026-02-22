import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from feedback.models import InterviewFeedback
from mock_tests.models import StudentAttempt
from accounts.models import User
from companies.models import Company
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Avg

@login_required
def generate_report(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    report_type = request.GET.get('type', 'feedback')
    alumni_id = request.GET.get('alumni_id')
    company_id = request.GET.get('company_id')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#1e3c72"),
        spaceAfter=20,
        alignment=1
    )
    
    elements.append(Paragraph("Placement Intelligence Report", title_style))
    elements.append(Paragraph(f"Generated on {User.objects.all()[0].date_joined.strftime('%B %d, %Y')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    if report_type == 'feedback':
        feedbacks = InterviewFeedback.objects.all()
        filter_desc = "All Contributions"
        
        if alumni_id:
            feedbacks = feedbacks.filter(alumni_id=alumni_id)
            alumni = get_object_or_404(User, id=alumni_id)
            filter_desc = f"Alumni: {alumni.get_full_name() or alumni.username}"
        
        if company_id:
            feedbacks = feedbacks.filter(company_id=company_id)
            company = get_object_or_404(Company, id=company_id)
            filter_desc += f" | Company: {company.name}"

        elements.append(Paragraph(f"Report Scope: {filter_desc}", styles['Heading2']))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("Feedback Summary", styles['Heading3']))
        data = [["Date", "Alumni", "Company", "Role", "Result"]]
        for f in feedbacks:
            data.append([
                f.interview_date.strftime("%Y-%m-%d"),
                f.alumni.username,
                f.company.name,
                f.job_role,
                f.status
            ])

        t = Table(data, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3c72")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        elements.append(Paragraph("Detailed Feedback Content", styles['Heading3']))
        for f in feedbacks:
            elements.append(Paragraph(f"{f.job_role} at {f.company.name} - by {f.alumni.username}", styles['Heading4']))
            details = [
                f"<b>Interview Date:</b> {f.interview_date.strftime('%Y-%m-%d')} | <b>Status:</b> {f.status} | <b>Package:</b> {f.salary_package or 'N/A'}",
                f"<b>Placement Type:</b> {f.get_placement_type_display()} | <b>Interview Type:</b> {f.get_interview_type_display()}",
                f"<b>Core Topics:</b> {f.core_technical_topics or 'N/A'}",
                f"<b>Overall Experience:</b> {f.overall_experience or 'N/A'}",
                f"<b>Advice/Tips:</b> {f.tips or 'N/A'}",
            ]
            for d in details:
                elements.append(Paragraph(d, styles['Normal']))
            elements.append(Spacer(1, 15))

    elif report_type == 'student':
        students = User.objects.filter(role='STUDENT')
        elements.append(Paragraph("Student Readiness Analysis", styles['Heading2']))
        elements.append(Spacer(1, 10))

        data = [["Student", "Tests Taken", "Avg Score", "Status"]]
        for student in students:
            attempts = StudentAttempt.objects.filter(student=student)
            count = attempts.count()
            avg = attempts.aggregate(Avg('score'))['score__avg'] or 0
            total_marks = attempts.aggregate(Avg('total_marks'))['total_marks__avg'] or 1
            perc = round((avg / total_marks) * 100, 1) if total_marks > 0 else 0
            
            status = "Ready" if perc >= 70 else "Needs Improvement"
            data.append([student.username, count, f"{perc}%", status])

        t = Table(data, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2ecc71")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(t)

    else:
        elements.append(Paragraph("System Comprehensive Audit", styles['Heading2']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"Total Active Students: {User.objects.filter(role='STUDENT').count()}", styles['Normal']))
        elements.append(Paragraph(f"Total Alumni Network: {User.objects.filter(role='ALUMNI').count()}", styles['Normal']))
        elements.append(Paragraph(f"Participating Companies: {Company.objects.count()}", styles['Normal']))
        elements.append(Paragraph(f"Knowledge Base Feedback: {InterviewFeedback.objects.count()}", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Strategic_Report.pdf')
