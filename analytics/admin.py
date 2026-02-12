from django.contrib import admin
from .models import ReadinessScore, SkillGap

@admin.register(ReadinessScore)
class ReadinessScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'overall_score', 'last_updated')

@admin.register(SkillGap)
class SkillGapAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill_name', 'current_level', 'required_level')
