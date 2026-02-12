from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'location', 'active_hiring', 'recruitment_drive_date')
    list_filter = ('industry', 'active_hiring')
    search_fields = ('name', 'required_skills')
