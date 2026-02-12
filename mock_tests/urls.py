from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestListView.as_view(), name='test_list'),
    path('<int:pk>/take/', views.take_test, name='take_test'),
    path('history/', views.test_history, name='test_history'),
]
