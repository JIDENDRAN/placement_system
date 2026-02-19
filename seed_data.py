import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_project.settings')
django.setup()

from accounts.models import User
from companies.models import Company
from feedback.models import InterviewFeedback, InterviewRound
from mock_tests.models import MockTest, Question
from mock_interviews.models import MockInterview, MockInterviewFeedback
from django.utils import timezone

def seed():
    print("🌱 Starting data seeding...")
    
    # ============= USERS =============
    print("👤 Creating users...")
    admin, _ = User.objects.get_or_create(
        username='admin', 
        defaults={'role': 'ADMIN', 'is_staff': True, 'is_superuser': True}
    )
    admin.set_password('admin123')
    admin.email = 'admin@placement.edu'
    admin.first_name = 'Admin'
    admin.last_name = 'User'
    admin.save()
    
    # Students
    student1, _ = User.objects.get_or_create(
        username='rajesh.kumar',
        defaults={'role': 'STUDENT', 'email': 'rajesh@student.edu', 'first_name': 'Rajesh', 'last_name': 'Kumar'}
    )
    student1.set_password('student123')
    student1.save()
    
    student2, _ = User.objects.get_or_create(
        username='priya.sharma',
        defaults={'role': 'STUDENT', 'email': 'priya@student.edu', 'first_name': 'Priya', 'last_name': 'Sharma'}
    )
    student2.set_password('student123')
    student2.save()
    
    # Alumni
    alumni1, _ = User.objects.get_or_create(
        username='ankit.verma',
        defaults={'role': 'ALUMNI', 'email': 'ankit@alumni.edu', 'first_name': 'Ankit', 'last_name': 'Verma'}
    )
    alumni1.set_password('alumni123')
    alumni1.save()
    from accounts.models import AlumniProfile
    AlumniProfile.objects.get_or_create(
        user=alumni1,
        defaults={'placed_company': 'Google', 'designation': 'Software Engineer', 'passout_year': 2024}
    )
    
    alumni2, _ = User.objects.get_or_create(
        username='sneha.reddy',
        defaults={'role': 'ALUMNI', 'email': 'sneha@alumni.edu', 'first_name': 'Sneha', 'last_name': 'Reddy'}
    )
    alumni2.set_password('alumni123')
    alumni2.save()
    AlumniProfile.objects.get_or_create(
        user=alumni2,
        defaults={'placed_company': 'Microsoft', 'designation': 'Software Development Engineer', 'passout_year': 2024}
    )

    # ============= COMPANIES =============
    print("🏢 Creating companies...")
    
    google, _ = Company.objects.get_or_create(
        name='Google',
        defaults={
            'industry': 'Technology',
            'location': 'Bangalore, Hyderabad, Gurgaon',
            'description': 'Google is a global technology leader focused on improving the ways people connect with information. Join us to work on products used by billions.',
            'required_skills': 'Data Structures, Algorithms, System Design, Python, Java, C++',
            'min_cgpa': 7.5,
            'ctc_range': '18-45 LPA',
            'recruitment_drive_date': datetime.date(2026, 8, 15),
            'active_hiring': True,
            'website': 'https://careers.google.com'
        }
    )
    
    microsoft, _ = Company.objects.get_or_create(
        name='Microsoft',
        defaults={
            'industry': 'Technology',
            'location': 'Bangalore, Hyderabad, Noida',
            'description': 'Microsoft empowers every person and organization on the planet to achieve more. Work on cutting-edge cloud, AI, and productivity solutions.',
            'required_skills': 'C#, .NET, Azure, System Design, Data Structures, Algorithms',
            'min_cgpa': 7.0,
            'ctc_range': '16-42 LPA',
            'recruitment_drive_date': datetime.date(2026, 9, 1),
            'active_hiring': True,
            'website': 'https://careers.microsoft.com'
        }
    )
    
    amazon, _ = Company.objects.get_or_create(
        name='Amazon',
        defaults={
            'industry': 'E-commerce & Cloud',
            'location': 'Bangalore, Hyderabad, Chennai',
            'description': 'Amazon is Earth\'s most customer-centric company. Work on AWS, e-commerce, and innovative technologies that impact millions.',
            'required_skills': 'Java, Python, Distributed Systems, AWS, Data Structures, Algorithms',
            'min_cgpa': 7.0,
            'ctc_range': '15-40 LPA',
            'recruitment_drive_date': datetime.date(2026, 7, 20),
            'active_hiring': True,
            'website': 'https://amazon.jobs'
        }
    )
    
    tcs, _ = Company.objects.get_or_create(
        name='TCS (Tata Consultancy Services)',
        defaults={
            'industry': 'IT Services & Consulting',
            'location': 'Pan India',
            'description': 'TCS is a leading global IT services, consulting, and business solutions organization. Part of the Tata Group, India\'s largest conglomerate.',
            'required_skills': 'Java, Python, SQL, Web Development, Problem Solving',
            'min_cgpa': 6.0,
            'ctc_range': '3.5-7 LPA',
            'recruitment_drive_date': datetime.date(2026, 6, 10),
            'active_hiring': True,
            'website': 'https://www.tcs.com/careers'
        }
    )
    
    infosys, _ = Company.objects.get_or_create(
        name='Infosys',
        defaults={
            'industry': 'IT Services & Consulting',
            'location': 'Bangalore, Pune, Mysore, Hyderabad',
            'description': 'Infosys is a global leader in next-generation digital services and consulting. Navigate your next with innovative solutions.',
            'required_skills': 'Java, Python, JavaScript, SQL, Cloud Technologies',
            'min_cgpa': 6.5,
            'ctc_range': '4-9 LPA',
            'recruitment_drive_date': datetime.date(2026, 6, 25),
            'active_hiring': True,
            'website': 'https://www.infosys.com/careers'
        }
    )
    
    wipro, _ = Company.objects.get_or_create(
        name='Wipro',
        defaults={
            'industry': 'IT Services & Consulting',
            'location': 'Bangalore, Hyderabad, Pune, Chennai',
            'description': 'Wipro is a leading technology services and consulting company focused on building innovative solutions that address clients\' most complex digital transformation needs.',
            'required_skills': 'Java, C++, Python, Database Management, Web Technologies',
            'min_cgpa': 6.0,
            'ctc_range': '3.5-7.5 LPA',
            'recruitment_drive_date': datetime.date(2026, 7, 5),
            'active_hiring': True,
            'website': 'https://careers.wipro.com'
        }
    )

    # ============= INTERVIEW FEEDBACKS =============
    print("📝 Creating interview feedbacks...")
    
    # Google Feedback
    google_feedback, created = InterviewFeedback.objects.get_or_create(
        alumni=alumni1,
        company=google,
        job_role='Software Engineer - L3',
        defaults={
            'salary_package': '28 LPA',
            'interview_date': datetime.date(2025, 11, 15),
            'rounds_count': 5,
            'core_technical_topics': 'Data Structures, Algorithms, System Design, Behavioral',
            'placement_type': 'ON',
            'interview_type': 'BOTH',
            'overall_experience': '''The Google interview process was rigorous but fair. It started with an online assessment focusing on DSA problems. 
            
After clearing that, I had 4 technical rounds and 1 HR round. The technical rounds covered:
- Round 1: Arrays, Strings, and Hash Maps
- Round 2: Trees, Graphs, and Dynamic Programming  
- Round 3: System Design - Design a URL Shortener
- Round 4: Behavioral + Coding - Leadership principles

The interviewers were friendly and gave hints when stuck. They valued the thought process more than the final solution.''',
            'overall_difficulty': 5,
            'status': 'SELECTED',
            'tips': 'Practice LeetCode medium/hard problems daily. Focus on explaining your approach clearly. For system design, understand scalability, load balancing, and database sharding.',
            'culture_fit_advice': 'Google values innovation, collaboration, and data-driven decision making. Be ready to discuss how you\'ve worked in teams and solved ambiguous problems.'
        }
    )
    
    if created:
        InterviewRound.objects.create(
            feedback=google_feedback,
            round_number=1,
            round_name='Online Assessment',
            questions_asked='Two coding problems: 1) Find longest substring without repeating characters 2) Merge K sorted linked lists',
            experience='90 minutes to solve. Managed to solve both with optimal solutions.'
        )
        InterviewRound.objects.create(
            feedback=google_feedback,
            round_number=3,
            round_name='System Design',
            questions_asked='Design a URL shortening service like bit.ly',
            experience='Discussed database schema, API design, caching strategies, and handling 1M requests/second. Interviewer was impressed with Redis caching approach.'
        )
    
    # Microsoft Feedback
    microsoft_feedback, created = InterviewFeedback.objects.get_or_create(
        alumni=alumni2,
        company=microsoft,
        job_role='Software Development Engineer',
        defaults={
            'salary_package': '24 LPA',
            'interview_date': datetime.date(2026, 1, 10),
            'rounds_count': 4,
            'core_technical_topics': 'OOP, Data Structures, Azure, Problem Solving',
            'placement_type': 'ON',
            'interview_type': 'TECH',
            'overall_experience': '''Microsoft's process was well-structured. Started with a coding round on their platform, followed by 3 technical interviews.

The focus was on:
- Clean code and OOP principles
- Problem-solving approach
- Understanding of cloud concepts (Azure)
- Real-world scenario questions

Each round was 45-60 minutes. Interviewers were very supportive and provided feedback during the interview itself.''',
            'overall_difficulty': 4,
            'status': 'SELECTED',
            'tips': 'Brush up on OOP concepts, SOLID principles, and design patterns. Have at least one project involving cloud services. Practice explaining your code clearly.',
            'culture_fit_advice': 'Microsoft looks for growth mindset and customer obsession. Share examples of how you\'ve learned from failures and put customers first.'
        }
    )
    
    # Amazon Feedback
    amazon_feedback, created = InterviewFeedback.objects.get_or_create(
        alumni=alumni1,
        company=amazon,
        job_role='SDE-1',
        defaults={
            'salary_package': '22 LPA',
            'interview_date': datetime.date(2025, 10, 20),
            'rounds_count': 4,
            'core_technical_topics': 'Leadership Principles, DSA, System Design, AWS',
            'placement_type': 'ON',
            'interview_type': 'BOTH',
            'overall_experience': '''Amazon's interview heavily focuses on their 16 Leadership Principles. Every round included behavioral questions using the STAR format.

Technical rounds covered:
- Coding: Arrays, Strings, Trees, Graphs
- System Design: Design Amazon's recommendation system
- Bar Raiser Round: Mix of behavioral and technical

The process was intense but the recruiters were very communicative throughout.''',
            'overall_difficulty': 4,
            'status': 'SELECTED',
            'tips': 'Memorize Amazon\'s Leadership Principles and prepare STAR stories for each. Practice medium-level LeetCode problems. Understand distributed systems basics.',
            'culture_fit_advice': 'Amazon values ownership, bias for action, and customer obsession. Demonstrate how you\'ve taken initiative and delivered results in past projects.'
        }
    )
    
    # TCS Feedback
    tcs_feedback, created = InterviewFeedback.objects.get_or_create(
        alumni=alumni2,
        company=tcs,
        job_role='Assistant System Engineer',
        defaults={
            'salary_package': '3.6 LPA',
            'interview_date': datetime.date(2025, 9, 5),
            'rounds_count': 3,
            'core_technical_topics': 'Aptitude, Technical MCQs, HR Interview',
            'placement_type': 'ON',
            'interview_type': 'BOTH',
            'overall_experience': '''TCS recruitment was straightforward with three rounds:

1. Aptitude Test: Quantitative, Logical Reasoning, Verbal
2. Technical MCQs: C, Java, DBMS, OS basics
3. HR Interview: Background, projects, willingness to relocate

The process was smooth and results were declared within a week. Good opportunity for freshers to start their career.''',
            'overall_difficulty': 2,
            'status': 'SELECTED',
            'tips': 'Focus on aptitude preparation - time management is key. Brush up on basic programming concepts and DBMS. Be confident in HR round.',
            'culture_fit_advice': 'TCS values dedication, learning attitude, and adaptability. Show willingness to learn new technologies and work in different domains.'
        }
    )

    # ============= MOCK TESTS =============
    print("📚 Creating mock tests...")
    
    # Google DSA Test
    google_test, created = MockTest.objects.get_or_create(
        title='Google - Data Structures & Algorithms',
        company=google,
        defaults={
            'description': 'Comprehensive test covering arrays, strings, trees, graphs, and dynamic programming - typical Google interview questions.',
            'duration_minutes': 60
        }
    )
    if created:
        Question.objects.create(
            test=google_test,
            text="What is the time complexity of binary search in a sorted array?",
            option_a="O(n)",
            option_b="O(log n)",
            option_c="O(n log n)",
            option_d="O(1)",
            correct_option='B',
            marks=5
        )
        Question.objects.create(
            test=google_test,
            text="Which data structure uses LIFO (Last In First Out) principle?",
            option_a="Queue",
            option_b="Linked List",
            option_c="Stack",
            option_d="Tree",
            correct_option='C',
            marks=5
        )
        Question.objects.create(
            test=google_test,
            text="What is the worst-case time complexity of QuickSort?",
            option_a="O(n)",
            option_b="O(n log n)",
            option_c="O(n²)",
            option_d="O(log n)",
            correct_option='C',
            marks=5
        )
        Question.objects.create(
            test=google_test,
            text="In a hash table with chaining, what is the average case time complexity for search?",
            option_a="O(1)",
            option_b="O(n)",
            option_c="O(log n)",
            option_d="O(n log n)",
            correct_option='A',
            marks=5
        )
        Question.objects.create(
            test=google_test,
            text="Which traversal of a binary tree visits nodes in ascending order for a BST?",
            option_a="Preorder",
            option_b="Inorder",
            option_c="Postorder",
            option_d="Level order",
            correct_option='B',
            marks=5
        )
    
    # Microsoft OOP Test
    microsoft_test, created = MockTest.objects.get_or_create(
        title='Microsoft - OOP & System Design Basics',
        company=microsoft,
        defaults={
            'description': 'Test focusing on Object-Oriented Programming concepts, design patterns, and system design fundamentals.',
            'duration_minutes': 45
        }
    )
    if created:
        Question.objects.create(
            test=microsoft_test,
            text="Which OOP principle allows a class to have multiple forms?",
            option_a="Encapsulation",
            option_b="Inheritance",
            option_c="Polymorphism",
            option_d="Abstraction",
            correct_option='C',
            marks=5
        )
        Question.objects.create(
            test=microsoft_test,
            text="What design pattern ensures a class has only one instance?",
            option_a="Factory",
            option_b="Singleton",
            option_c="Observer",
            option_d="Strategy",
            correct_option='B',
            marks=5
        )
        Question.objects.create(
            test=microsoft_test,
            text="Which SOLID principle states that a class should have only one reason to change?",
            option_a="Single Responsibility Principle",
            option_b="Open/Closed Principle",
            option_c="Liskov Substitution Principle",
            option_d="Dependency Inversion Principle",
            correct_option='A',
            marks=5
        )
    
    # Amazon Leadership Test
    amazon_test, created = MockTest.objects.get_or_create(
        title='Amazon - Leadership Principles & Problem Solving',
        company=amazon,
        defaults={
            'description': 'Test covering Amazon\'s Leadership Principles, logical reasoning, and problem-solving scenarios.',
            'duration_minutes': 40
        }
    )
    if created:
        Question.objects.create(
            test=amazon_test,
            text="Which Amazon Leadership Principle emphasizes delivering results even when it's difficult?",
            option_a="Customer Obsession",
            option_b="Bias for Action",
            option_c="Deliver Results",
            option_d="Ownership",
            correct_option='C',
            marks=5
        )
        Question.objects.create(
            test=amazon_test,
            text="In distributed systems, what does CAP theorem stand for?",
            option_a="Consistency, Availability, Partition tolerance",
            option_b="Cache, API, Performance",
            option_c="Compute, Analyze, Process",
            option_d="Cloud, Application, Platform",
            correct_option='A',
            marks=5
        )
    
    # TCS Aptitude Test
    tcs_test, created = MockTest.objects.get_or_create(
        title='TCS - Aptitude & Technical MCQs',
        company=tcs,
        defaults={
            'description': 'General aptitude test covering quantitative aptitude, logical reasoning, and basic technical concepts.',
            'duration_minutes': 90
        }
    )
    if created:
        Question.objects.create(
            test=tcs_test,
            text="If a train travels 120 km in 2 hours, what is its average speed?",
            option_a="50 km/h",
            option_b="60 km/h",
            option_c="70 km/h",
            option_d="80 km/h",
            correct_option='B',
            marks=3
        )
        Question.objects.create(
            test=tcs_test,
            text="What is the output of: print(type([]) == list) in Python?",
            option_a="True",
            option_b="False",
            option_c="Error",
            option_d="None",
            correct_option='A',
            marks=3
        )
        Question.objects.create(
            test=tcs_test,
            text="Which SQL command is used to retrieve data from a database?",
            option_a="GET",
            option_b="FETCH",
            option_c="SELECT",
            option_d="RETRIEVE",
            correct_option='C',
            marks=3
        )

    # ============= MOCK INTERVIEWS =============
    print("🎤 Creating mock interviews...")
    
    # Scheduled Interview
    mock_interview1, created = MockInterview.objects.get_or_create(
        student=student1,
        interviewer=alumni1,
        company=google,
        defaults={
            'topic': 'System Design - Design Instagram',
            'scheduled_at': timezone.now() + timezone.timedelta(days=2),
            'duration_minutes': 60,
            'status': 'SCHEDULED',
            'meeting_link': 'https://meet.google.com/xyz-abcd-efg',
            'notes': ''
        }
    )
    
    # Completed Interview with Feedback
    mock_interview2, created = MockInterview.objects.get_or_create(
        student=student1,
        interviewer=alumni2,
        company=microsoft,
        defaults={
            'topic': 'DSA - Trees and Graphs',
            'scheduled_at': timezone.now() - timezone.timedelta(days=3),
            'duration_minutes': 45,
            'status': 'COMPLETED',
            'meeting_link': 'https://teams.microsoft.com/meet/abc123',
            'notes': 'Student showed good understanding of tree traversals. Needs practice on graph algorithms like Dijkstra and Floyd-Warshall.'
        }
    )
    
    if created:
        MockInterviewFeedback.objects.create(
            interview=mock_interview2,
            technical_score=7,
            communication_score=8,
            behavioral_score=8,
            problem_solving_score=7,
            strengths='''- Clear communication and thought process explanation
- Good grasp of tree data structures (BST, AVL)
- Able to optimize brute force solutions
- Confident and composed during the session''',
            areas_of_improvement='''- Practice more graph algorithms (BFS, DFS, shortest path)
- Work on time complexity analysis
- Study dynamic programming patterns
- Improve edge case handling''',
            overall_comments='''Rajesh is on the right track. With focused practice on graphs and DP, he'll be ready for product-based company interviews in 2-3 weeks. 

Recommended next steps:
1. Solve 20 graph problems on LeetCode
2. Complete Striver's DP playlist
3. Take another mock on System Design''',
            is_ready_for_real_interview=False
        )
    
    # Another completed interview
    mock_interview3, created = MockInterview.objects.get_or_create(
        student=student2,
        interviewer=alumni1,
        company=amazon,
        defaults={
            'topic': 'Behavioral - Amazon Leadership Principles',
            'scheduled_at': timezone.now() - timezone.timedelta(days=1),
            'duration_minutes': 45,
            'status': 'COMPLETED',
            'meeting_link': 'https://chime.aws/meet/priya-mock',
            'notes': 'Excellent STAR format responses. Ready for Amazon interviews.'
        }
    )
    
    if created:
        MockInterviewFeedback.objects.create(
            interview=mock_interview3,
            technical_score=9,
            communication_score=9,
            behavioral_score=10,
            problem_solving_score=8,
            strengths='''- Outstanding behavioral interview skills
- Perfect STAR format usage
- Demonstrated all 16 Amazon Leadership Principles with real examples
- Confident and articulate
- Great project portfolio''',
            areas_of_improvement='''- Minor: Could add more quantitative metrics to stories
- Practice a few more system design scenarios
- Brush up on AWS services (S3, EC2, Lambda)''',
            overall_comments='''Priya is exceptionally well-prepared for Amazon interviews. Her behavioral responses were textbook perfect, and she clearly understands what Amazon looks for.

She's interview-ready and should apply immediately. Recommended to target SDE-1 roles at Amazon, Microsoft, and Google.

Confidence level: 95%''',
            is_ready_for_real_interview=True
        )

    print("✅ Data seeding completed successfully!")
    print(f"   - Created {User.objects.count()} users")
    print(f"   - Created {Company.objects.count()} companies")
    print(f"   - Created {InterviewFeedback.objects.count()} interview feedbacks")
    print(f"   - Created {MockTest.objects.count()} mock tests")
    print(f"   - Created {Question.objects.count()} questions")
    print(f"   - Created {MockInterview.objects.count()} mock interviews")
    print(f"   - Created {MockInterviewFeedback.objects.count()} interview feedbacks")

if __name__ == '__main__':
    seed()
