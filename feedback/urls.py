from django.urls import path
from . import views

urlpatterns = [
    path('', views.FeedbackListView.as_view(), name='feedback_list'),
    path('<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback_detail'),
    path('add/', views.FeedbackCreateView.as_view(), name='feedback_create'),
]
