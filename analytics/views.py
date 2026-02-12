from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mock_tests.models import StudentAttempt
from .models import ReadinessScore, SkillGap
import csv
from django.http import HttpResponse

@login_required
def analytics_dashboard(request):
    attempts = StudentAttempt.objects.filter(student=request.user)
    scores = [a.score for a in attempts]
    labels = [a.test.title for a in attempts]
    
    context = {
        'scores': scores,
        'labels': labels,
        'attempts': attempts,
    }
    return render(request, 'analytics/dashboard.html', context)

@login_required
def export_csv_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="placement_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Test Title', 'Score', 'Total Marks', 'Date'])
    
    attempts = StudentAttempt.objects.filter(student=request.user)
    for attempt in attempts:
        writer.writerow([attempt.test.title, attempt.score, attempt.total_marks, attempt.completed_at])
    
    return response

# Placeholder for PDF report
# In production, use reportlab or weasyprint
@login_required
def export_pdf_report(request):
    from reportlab.pdfgen import canvas
    from io import BytesIO
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, f"Placement Readiness Report for {request.user.username}")
    
    attempts = StudentAttempt.objects.filter(student=request.user)
    y = 700
    for a in attempts:
        p.drawString(100, y, f"{a.test.title}: {a.score}/{a.total_marks} on {a.completed_at.date()}")
        y -= 20
        
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
