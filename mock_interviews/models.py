from django.db import models
from django.conf import settings
from companies.models import Company

class MockInterview(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mock_interviews_as_student',
        limit_choices_to={'role': 'STUDENT'}
    )
    interviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        related_name='mock_interviews_as_interviewer',
        limit_choices_to={'role__in': ['ADMIN', 'ALUMNI']},
        null=True,
        blank=True
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='mock_interviews'
    )
    topic = models.CharField(max_length=200, help_text="e.g. Python Backend, Frontend React, Data Structures")
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=45)
    meeting_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    
    # Session Details
    notes = models.TextField(blank=True, null=True, help_text="Interviewer notes during the session")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mock Interview: {self.student.username} - {self.topic}"

class MockInterviewFeedback(models.Model):
    interview = models.OneToOneField(MockInterview, on_delete=models.CASCADE, related_name='feedback')
    technical_score = models.IntegerField(default=0, help_text="Scale 1-10")
    communication_score = models.IntegerField(default=0, help_text="Scale 1-10")
    behavioral_score = models.IntegerField(default=0, help_text="Scale 1-10")
    problem_solving_score = models.IntegerField(default=0, help_text="Scale 1-10")
    
    strengths = models.TextField()
    areas_of_improvement = models.TextField()
    overall_comments = models.TextField()
    
    is_ready_for_real_interview = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.interview.student.username} - {self.interview.topic}"
