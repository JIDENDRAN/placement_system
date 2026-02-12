from django.db import models
from django.conf import settings

class ReadinessScore(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='readiness_score')
    aptitude_score = models.FloatField(default=0.0)
    technical_score = models.FloatField(default=0.0)
    communication_score = models.FloatField(default=0.0)
    overall_score = models.FloatField(default=0.0)
    
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} readiness: {self.overall_score}"

class SkillGap(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skill_gaps')
    skill_name = models.CharField(max_length=100)
    current_level = models.IntegerField(default=1, help_text="Rating 1-10")
    required_level = models.IntegerField(default=8)
    gap_analysis = models.TextField()

    def __str__(self):
        return f"{self.student.username} gap in {self.skill_name}"
