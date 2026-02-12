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
    interview_date = models.DateField()
    overall_experience = models.TextField()
    overall_difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=3)
    status = models.CharField(max_length=50, choices=(('SELECTED', 'Selected'), ('REJECTED', 'Rejected'), ('PENDING', 'Pending')), default='SELECTED')
    tips = models.TextField(blank=True, null=True)
    
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
