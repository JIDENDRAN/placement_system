import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_project.settings')
django.setup()

from accounts.models import User
from companies.models import Company
from feedback.models import InterviewFeedback
from mock_tests.models import MockTest, Question

def seed():
    # Create Admin
    admin, _ = User.objects.get_or_create(username='admin', role='ADMIN', is_staff=True, is_superuser=True)
    admin.set_password('admin123')
    admin.save()
    
    # Create Student
    student, _ = User.objects.get_or_create(username='student1', role='STUDENT')
    student.set_password('student123')
    student.save()
    
    # Create Alumni
    alumni, _ = User.objects.get_or_create(username='alumni1', role='ALUMNI')
    alumni.set_password('alumni123')
    alumni.save()

    # Create Companies
    google, _ = Company.objects.get_or_create(
        name='Google', 
        industry='Tech', 
        location='Bangalore', 
        description='Leading tech giant.',
        required_skills='Python, Algorithms, Data Structures'
    )
    amazon, _ = Company.objects.get_or_create(
        name='Amazon', 
        industry='E-commerce', 
        location='Hyderabad', 
        description='Customer centric company.',
        required_skills='Java, Distributed Systems'
    )

    # Create Feedbacks
    InterviewFeedback.objects.get_or_create(
        alumni=alumni,
        company=google,
        job_role='Software Engineer',
        interview_date=datetime.date(2025, 12, 1),
        overall_experience='It was a great experience. 5 rounds of technical questions.',
        overall_difficulty=4,
        status='SELECTED'
    )

    # Create Mock Tests
    test, created = MockTest.objects.get_or_create(
        title='Google Aptitude Test',
        company=google,
        description='A test covering basic aptitude and programming logic.',
        duration_minutes=30
    )
    if created:
        Question.objects.create(
            test=test,
            text="What is the time complexity of binary search?",
            option_a="O(n)",
            option_b="O(log n)",
            option_c="O(n log n)",
            option_d="O(1)",
            correct_option='B',
            marks=5
        )
        Question.objects.create(
            test=test,
            text="Which data structure uses LIFO?",
            option_a="Queue",
            option_b="Linked List",
            option_c="Stack",
            option_d="Tree",
            correct_option='C',
            marks=5
        )

    print("Data seeded successfully!")

if __name__ == '__main__':
    seed()
