from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='company_list'),
    path('<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('add/', views.CompanyCreateView.as_view(), name='company_create'),
    path('<int:pk>/edit/', views.CompanyUpdateView.as_view(), name='company_edit'),
]
