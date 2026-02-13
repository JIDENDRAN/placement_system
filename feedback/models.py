from django.db import models
from django.conf import settings
from companies.models import Company

class InterviewFeedback(models.Model):
    DIFFICULTY_CHOICES = (
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Medium'),
        (4, 'Hard'),
        (5, 'Very Hard'),
    )
    
    alumni = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='feedbacks')
    job_role = models.CharField(max_length=200)
    salary_package = models.CharField(max_length=100, help_text="e.g. 12 LPA", blank=True, null=True)
    interview_date = models.DateField()
    rounds_count = models.IntegerField(default=1, help_text="Total number of rounds")
    core_technical_topics = models.TextField(help_text="Comma separated topics like React, AWS, OS", blank=True, null=True)
    
    PLACEMENT_TYPE_CHOICES = (
        ('ON', 'On-Campus'),
        ('OFF', 'Off-Campus'),
        ('REF', 'Referral'),
        ('INT', 'Internal/Other'),
    )
    placement_type = models.CharField(max_length=3, choices=PLACEMENT_TYPE_CHOICES, default='ON')
    
    INTERVIEW_TYPE_CHOICES = (
        ('TECH', 'Technical'),
        ('HR', 'HR'),
        ('BOTH', 'Technical + HR'),
        ('MNG', 'Managerial'),
    )
    interview_type = models.CharField(max_length=4, choices=INTERVIEW_TYPE_CHOICES, default='TECH')
    
    overall_experience = models.TextField()
    overall_difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=3)
    status = models.CharField(max_length=50, choices=(('SELECTED', 'Selected'), ('REJECTED', 'Rejected'), ('PENDING', 'Pending')), default='SELECTED')
    tips = models.TextField(help_text="General preparation advice", blank=True, null=True)
    culture_fit_advice = models.TextField(help_text="What is the company culture like?", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_role} at {self.company.name} - {self.alumni.username}"

class InterviewRound(models.Model):
    feedback = models.ForeignKey(InterviewFeedback, on_delete=models.CASCADE, related_name='rounds')
    round_number = models.PositiveIntegerField()
    round_name = models.CharField(max_length=100) # e.g. Technical HR, Group Discussion
    questions_asked = models.TextField()
    experience = models.TextField()
    
    def __str__(self):
        return f"Round {self.round_number} for {self.feedback.company.name}"
