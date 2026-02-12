from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import MockTest, Question, StudentAttempt
from django.contrib import messages

class TestListView(ListView):
    model = MockTest
    template_name = 'mock_tests/test_list.html'
    context_object_name = 'tests'

@login_required
def take_test(request, pk):
    test = get_object_or_404(MockTest, pk=pk)
    questions = test.questions.all()
    
    if request.method == 'POST':
        score = 0
        total_marks = 0
        for q in questions:
            total_marks += q.marks
            answer = request.POST.get(f'question_{q.id}')
            if answer == q.correct_option:
                score += q.marks
        
        attempt = StudentAttempt.objects.create(
            student=request.user,
            test=test,
            score=score,
            total_marks=total_marks
        )
        return render(request, 'mock_tests/test_result.html', {'attempt': attempt})
    
    return render(request, 'mock_tests/take_test.html', {'test': test, 'questions': questions})

@login_required
def test_history(request):
    attempts = StudentAttempt.objects.filter(student=request.user).order_by('-completed_at')
    return render(request, 'mock_tests/test_history.html', {'attempts': attempts})
