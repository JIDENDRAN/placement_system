from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('STUDENT', 'Student'),
        ('ALUMNI', 'Alumni'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    department = models.CharField(max_length=100)
    batch = models.CharField(max_length=10)
    cgpa = models.FloatField(default=0.0)
    skills = models.TextField(help_text="Comma separated list of skills")
    repository_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    def __str__(self):
        return f"Student: {self.user.username}"

class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni_profile')
    placed_company = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    passout_year = models.IntegerField()
    linkedin_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Alumni: {self.user.username} at {self.placed_company}"
