from django.urls import path
from . import views

urlpatterns = [
    path('', views.InterviewListView.as_view(), name='interview_list'),
    path('schedule/', views.ScheduleInterviewView.as_view(), name='schedule_interview'),
    path('<int:pk>/', views.interview_detail, name='interview_detail'),
    path('<int:pk>/feedback/', views.submit_feedback, name='submit_feedback'),
]
