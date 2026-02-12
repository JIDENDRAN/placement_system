from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # Eligibility & Requirements
    industry = models.CharField(max_length=100)
    min_cgpa = models.FloatField(default=0.0)
    required_skills = models.TextField(help_text="Comma separated skills")
    
    # Recruitment details
    recruitment_drive_date = models.DateField(blank=True, null=True)
    ctc_range = models.CharField(max_length=100, help_text="e.g. 5-8 LPA")
    active_hiring = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"
