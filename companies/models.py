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

    @property
    def location_list(self):
        return [loc.strip() for loc in self.location.split(',') if loc.strip()]

    def get_location_summary_html(self):
        from django.utils.safestring import mark_safe
        locs = self.location_list
        badges = []
        for loc in locs[:2]:
            badges.append(f'<span class="badge bg-light text-dark shadow-none border"><i class="bi bi-geo-alt me-1"></i>{loc}</span>')
        
        if len(locs) > 2:
            badges.append(f'<span class="badge bg-light text-dark shadow-none border">+{len(locs)-2} more</span>')
        
        return mark_safe(" ".join(badges))

    def get_all_locations_html(self):
        from django.utils.safestring import mark_safe
        locs = self.location_list
        badges = [f'<span class="badge bg-white text-dark border fw-normal me-1 mb-1">{loc}</span>' for loc in locs]
        return mark_safe(" ".join(badges))

    def get_location_header_html(self):
        from django.utils.safestring import mark_safe
        locs = self.location_list
        parts = [f'<span class="text-secondary fw-medium"><i class="bi bi-geo-alt-fill text-danger me-1"></i>{loc}</span>' for loc in locs]
        return mark_safe('<span class="mx-2 text-muted">|</span>'.join(parts))

    class Meta:
        verbose_name_plural = "Companies"
