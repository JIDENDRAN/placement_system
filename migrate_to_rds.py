"""
SQLite to AWS RDS PostgreSQL Migration Script
=============================================
This script exports data from your local SQLite database
and imports it into your AWS RDS PostgreSQL database.

Usage:
    1. Make sure your .env file has DATABASE_URL pointing to RDS
    2. Run: .\venv\Scripts\python migrate_to_rds.py

Prerequisites:
    - Local SQLite database (db.sqlite3) exists with data
    - RDS endpoint is accessible (Security Group configured)
    - DATABASE_URL is set in .env file
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent
DUMP_FILE = BASE_DIR / 'data_dump.json'
PYTHON = BASE_DIR / 'venv' / 'Scripts' / 'python.exe'
MANAGE = BASE_DIR / 'manage.py'


def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_step(step_num, text):
    print(f"\n[Step {step_num}] {text}")
    print("-" * 40)


def run_command(cmd, env=None):
    """Run a command and return success status."""
    result = subprocess.run(
        cmd,
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
        env=env or os.environ
    )
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        return False
    return True


def main():
    print_header("SQLite → AWS RDS PostgreSQL Migration")
    
    # Step 1: Check prerequisites
    print_step(1, "Checking prerequisites...")
    
    if not (BASE_DIR / 'db.sqlite3').exists():
        print("ERROR: db.sqlite3 not found! No local data to migrate.")
        sys.exit(1)
    print("✓ SQLite database found")
    
    if not PYTHON.exists():
        print("ERROR: Virtual environment not found!")
        sys.exit(1)
    print("✓ Virtual environment found")
    
    # Step 2: Export data from SQLite
    print_step(2, "Exporting data from SQLite...")
    
    # Temporarily remove DATABASE_URL so Django uses SQLite
    env_sqlite = os.environ.copy()
    env_sqlite.pop('DATABASE_URL', None)
    
    dump_cmd = [
        str(PYTHON), str(MANAGE), 'dumpdata',
        '--natural-foreign', '--natural-primary',
        '--exclude=contenttypes',
        '--exclude=auth.permission',
        '--exclude=admin.logentry',
        '--exclude=sessions.session',
        '--indent=2',
        f'--output={DUMP_FILE}'
    ]
    
    if not run_command(dump_cmd, env=env_sqlite):
        print("ERROR: Failed to export data from SQLite!")
        sys.exit(1)
    
    # Check dump file
    if not DUMP_FILE.exists() or DUMP_FILE.stat().st_size == 0:
        print("ERROR: Data dump file is empty or not created!")
        sys.exit(1)
    
    file_size = DUMP_FILE.stat().st_size / 1024  # KB
    print(f"✓ Data exported successfully ({file_size:.1f} KB)")
    
    # Count records
    with open(DUMP_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ Total records: {len(data)}")
    
    # Step 3: Check DATABASE_URL
    print_step(3, "Checking RDS connection...")
    
    # Load .env file
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
    
    db_url = os.getenv('DATABASE_URL', '')
    if 'postgres' not in db_url:
        print("ERROR: DATABASE_URL is not set or not pointing to PostgreSQL!")
        print("Please set DATABASE_URL in your .env file:")
        print("  DATABASE_URL=postgres://user:pass@your-rds-endpoint:5432/placement_db")
        sys.exit(1)
    
    # Mask password for display
    display_url = db_url
    if '@' in db_url:
        parts = db_url.split('@')
        cred_parts = parts[0].split(':')
        if len(cred_parts) >= 3:
            display_url = f"{cred_parts[0]}:{cred_parts[1]}:****@{parts[1]}"
    print(f"✓ DATABASE_URL: {display_url}")
    
    # Step 4: Run migrations on RDS
    print_step(4, "Running migrations on RDS...")
    
    if not run_command([str(PYTHON), str(MANAGE), 'migrate']):
        print("ERROR: Failed to run migrations on RDS!")
        print("Check your DATABASE_URL, Security Group, and RDS status.")
        sys.exit(1)
    print("✓ Migrations completed on RDS")
    
    # Step 5: Load data into RDS
    print_step(5, "Loading data into RDS PostgreSQL...")
    
    if not run_command([str(PYTHON), str(MANAGE), 'loaddata', str(DUMP_FILE)]):
        print("ERROR: Failed to load data into RDS!")
        print("This could be due to data conflicts. Try running:")
        print(f"  .\\venv\\Scripts\\python manage.py loaddata {DUMP_FILE}")
        sys.exit(1)
    
    print("✓ Data loaded successfully into RDS!")
    
    # Step 6: Verify
    print_step(6, "Verifying migration...")
    
    verify_cmd = [
        str(PYTHON), '-c',
        'import django; '
        'import os; '
        'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "placement_project.settings"); '
        'django.setup(); '
        'from django.db import connection; '
        'print(f"Database: {connection.vendor}"); '
        'from accounts.models import User; '
        'print(f"Users: {User.objects.count()}"); '
        'from companies.models import Company; '
        'print(f"Companies: {Company.objects.count()}"); '
        'from feedback.models import InterviewFeedback; '
        'print(f"Feedbacks: {InterviewFeedback.objects.count()}"); '
        'from mock_tests.models import MockTest; '
        'print(f"Mock Tests: {MockTest.objects.count()}"); '
        'from mock_interviews.models import MockInterview; '
        'print(f"Mock Interviews: {MockInterview.objects.count()}"); '
    ]
    
    run_command(verify_cmd)
    
    # Done!
    print_header("Migration Complete! 🎉")
    print("Your data has been migrated from SQLite to AWS RDS PostgreSQL.")
    print("\nNext steps:")
    print("  1. Start your server: .\\venv\\Scripts\\python manage.py runserver")
    print("  2. Verify the app works correctly in the browser")
    print("  3. Check data in the admin panel: http://127.0.0.1:8000/admin/")
    print(f"\nBackup file saved: {DUMP_FILE}")
    print("You can safely keep db.sqlite3 as a backup.\n")


if __name__ == '__main__':
    main()
