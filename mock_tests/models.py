from django.db import models
from django.conf import settings
from companies.models import Company

class MockTest(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='mock_tests', blank=True, null=True)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=(('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')))
    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Q: {self.text[:50]}..."

class StudentAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attempts')
    test = models.ForeignKey(MockTest, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.test.title} - {self.score}/{self.total_marks}"
