import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_project.settings')
django.setup()

from accounts.models import User, StudentProfile, AlumniProfile

def create_bulk_accounts():
    print("🚀 Starting bulk account creation...")
    
    # Password for all accounts
    password = "Password123"
    
    # 1. Create 150 Student accounts
    print(f"👨‍🎓 Creating 150 student accounts...")
    student_count = 0
    departments = ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil"]
    batches = ["2020-2024", "2021-2025", "2022-2026", "2023-2027"]
    
    for i in range(1, 151):
        username = f"student_{i:03d}"
        email = f"{username}@student.edu"
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'role': 'STUDENT',
                'first_name': f'Student',
                'last_name': f'{i:03d}'
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            
        # Ensure student profile exists
        StudentProfile.objects.get_or_create(
            user=user,
            defaults={
                'department': random.choice(departments),
                'batch': random.choice(batches),
                'cgpa': round(random.uniform(6.5, 9.8), 2),
                'skills': "Python, Django, SQL, JavaScript"
            }
        )
        if created:
            student_count += 1
            if student_count % 50 == 0:
                print(f"   - Created {student_count} new students...")
    
    print(f"✅ Total new students created: {student_count}")
    
    # 2. Create 300 Alumni accounts
    print(f"🎓 Creating 300 alumni accounts...")
    alumni_count = 0
    companies = ["Google", "Microsoft", "Amazon", "TCS", "Infosys", "Wipro", "Meta", "Apple"]
    designations = ["Software Engineer", "Frontend Developer", "Backend Developer", "Data Analyst", "Project Manager"]
    
    for i in range(1, 301):
        username = f"alumni_{i:03d}"
        email = f"{username}@alumni.edu"
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'role': 'ALUMNI',
                'first_name': f'Alumni',
                'last_name': f'{i:03d}'
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            
        # Ensure alumni profile exists
        AlumniProfile.objects.get_or_create(
            user=user,
            defaults={
                'placed_company': random.choice(companies),
                'designation': random.choice(designations),
                'passout_year': random.randint(2018, 2024)
            }
        )
        if created:
            alumni_count += 1
            if alumni_count % 50 == 0:
                print(f"   - Created {alumni_count} new alumni...")
                
    print(f"✅ Total alumni created: {alumni_count}")
    print("\n🎉 Bulk account creation finished successfully!")

if __name__ == "__main__":
    create_bulk_accounts()
