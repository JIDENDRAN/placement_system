from django.contrib import admin
from .models import InterviewFeedback, InterviewRound

class InterviewRoundInline(admin.TabularInline):
    model = InterviewRound
    extra = 1

@admin.register(InterviewFeedback)
class InterviewFeedbackAdmin(admin.ModelAdmin):
    list_display = ('company', 'alumni', 'job_role', 'overall_difficulty', 'status', 'created_at')
    list_filter = ('status', 'overall_difficulty', 'company')
    search_fields = ('job_role', 'overall_experience')
    inlines = [InterviewRoundInline]
