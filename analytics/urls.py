from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    path('export/csv/', views.export_csv_report, name='export_csv'),
    path('export/pdf/', views.export_pdf_report, name='export_pdf'),
]
