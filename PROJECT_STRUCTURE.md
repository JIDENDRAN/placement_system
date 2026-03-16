# Centralized Cloud System for Student Placement Readiness Monitoring

## Project Structure

```
placement_system/
│
├── placement_project/              # Main Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                       # User authentication & management
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                  # User, Profile models
│   ├── views.py                   # Login, Register, Dashboard
│   ├── urls.py
│   ├── forms.py                   # Registration, Login forms
│   ├── admin.py
│   └── templates/
│       └── accounts/
│           ├── login.html
│           ├── register.html
│           ├── admin_dashboard.html
│           ├── student_dashboard.html
│           └── alumni_dashboard.html
│
├── companies/                      # Company management
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                  # Company model
│   ├── views.py                   # CRUD operations
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── companies/
│           ├── company_list.html
│           ├── company_detail.html
│           ├── company_form.html
│           └── company_search.html
│
├── feedback/                       # Interview feedback module
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                  # Feedback, InterviewRound models
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── feedback/
│           ├── feedback_list.html
│           ├── feedback_detail.html
│           ├── feedback_form.html
│           └── feedback_search.html
│
├── mock_tests/                     # Mock test engine
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                  # Test, Question, StudentAttempt models
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── mock_tests/
│           ├── test_list.html
│           ├── test_detail.html
│           ├── take_test.html
│           ├── test_result.html
│           └── test_history.html
│
├── analytics/                      # Analytics & reporting
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                  # ReadinessScore, SkillGap models
│   ├── views.py
│   ├── urls.py
│   ├── utils.py                   # Analytics calculations
│   ├── admin.py
│   └── templates/
│       └── analytics/
│           ├── dashboard.html
│           ├── skill_gap.html
│           ├── performance_charts.html
│           └── reports.html
│
├── static/                         # Static files
│   ├── css/
│   │   ├── style.css
│   │   └── dashboard.css
│   ├── js/
│   │   ├── main.js
│   │   └── charts.js
│   └── images/
│       └── logo.png
│
├── templates/                      # Global templates
│   ├── base.html
│   ├── navbar.html
│   ├── footer.html
│   └── home.html
│
├── media/                          # User uploaded files
│   └── company_logos/
│
├── requirements.txt                # Python dependencies
├── manage.py                       # Django management script
├── .env                           # Environment variables
├── .gitignore
└── README.md
```

## Apps Breakdown

### 1. accounts
- User authentication (login, register, logout)
- Role-based access control (Admin, Student, Alumni)
- User profile management
- Custom user model with role field

### 2. companies
- Company CRUD operations
- Company profiles
- Eligibility criteria
- Skills required
- Recruitment drive details

### 3. feedback
- Interview feedback submission (by alumni)
- Round-wise feedback
- Questions asked
- Tips and difficulty ratings
- Feedback search and filter

### 4. mock_tests
- Create company-specific tests
- MCQ-based questions
- Auto-evaluation system
- Score storage and history
- Timed tests

### 5. analytics
- Performance charts (Chart.js)
- Skill gap analysis
- Success probability calculation
- Readiness score tracking
- Company-wise preparation stats
- CSV/PDF report export

## Technology Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: PostgreSQL (AWS RDS - Primary Database)
- **Charts**: Chart.js
- **PDF Generation**: ReportLab / WeasyPrint
- **Authentication**: Django built-in auth with custom user model
- **Cloud**: AWS (EC2, RDS, S3)

## Key Features

✅ Role-based authentication and authorization
✅ Company management system
✅ Interview feedback sharing
✅ Mock test engine with auto-grading
✅ Analytics dashboard with charts
✅ Skill gap analysis
✅ Readiness score calculation
✅ CSV/PDF export functionality
✅ Responsive design with Bootstrap
✅ Search and filter capabilities
✅ Pagination for large datasets
✅ Admin panel customization
✅ Secure user authentication
✅ Cloud deployment ready
