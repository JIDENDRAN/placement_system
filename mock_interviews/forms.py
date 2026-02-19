from django import forms
from .models import MockInterview

class MockInterviewForm(forms.ModelForm):
    class Meta:
        model = MockInterview
        fields = ['student', 'interviewer', 'company', 'topic', 'scheduled_at', 'duration_minutes', 'meeting_link']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'interviewer': forms.Select(attrs={'class': 'form-select'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. System Design'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://zoom.us/j/...'}),
        }
