from django.contrib import admin
from .models import MockTest, Question, StudentAttempt

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5

@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'duration_minutes', 'created_at')
    inlines = [QuestionInline]

@admin.register(StudentAttempt)
class StudentAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'total_marks', 'completed_at')
    list_filter = ('test', 'student')
