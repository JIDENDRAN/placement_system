# 🚀 AWS RDS PostgreSQL Setup Guide — Placement System

## Table of Contents
1. [Create AWS Account](#1-create-aws-account)
2. [Set Up AWS RDS PostgreSQL](#2-set-up-aws-rds-postgresql)
3. [Configure Security Group](#3-configure-security-group)
4. [Connect Django to RDS](#4-connect-django-to-rds)
5. [Migrate Data from SQLite to RDS](#5-migrate-data-from-sqlite-to-rds)
6. [Set Up S3 for Media Files](#6-set-up-s3-for-media-files-optional)
7. [Verify Everything Works](#7-verify-everything-works)
8. [Cost Estimation](#8-cost-estimation)

---

## 1. Create AWS Account

If you don't already have an AWS account:

1. Go to **https://aws.amazon.com/**
2. Click **"Create an AWS Account"**
3. Enter your **email address** and choose an **account name**
4. Enter your **credit/debit card** details (required, but AWS Free Tier is available)
5. Complete phone verification
6. Choose **"Basic Support - Free"** plan
7. Sign in to the **AWS Management Console**

> 💡 **Free Tier**: AWS RDS PostgreSQL includes **750 hours/month of db.t3.micro** for 12 months — that's essentially free for 1 year!

---

## 2. Set Up AWS RDS PostgreSQL

### Step 2.1 — Navigate to RDS
1. Sign in to **AWS Console**: https://console.aws.amazon.com/
2. In the top search bar, type **"RDS"** and click **Amazon RDS**
3. Make sure you select a **Region** close to your users (top-right corner)
   - For India: Choose **Asia Pacific (Mumbai) — ap-south-1**

### Step 2.2 — Create Database
1. Click **"Create database"** button
2. Choose the following settings:

#### Database Creation Method
- ✅ Select **"Standard create"**

#### Engine Options
- ✅ Select **PostgreSQL**
- Version: **PostgreSQL 15.x** (latest stable)

#### Templates
- ✅ Select **"Free tier"** (for learning/development)
  - For production later, choose "Production"

#### Settings
| Setting | Value |
|---------|-------|
| DB instance identifier | `placement-system-db` |
| Master username | `placementadmin` |
| Master password | Choose a **strong password** (SAVE THIS!) |
| Confirm password | Re-enter the password |

> ⚠️ **IMPORTANT**: Save the master username and password somewhere safe. You'll need them later!

#### Instance Configuration
- DB instance class: **db.t3.micro** (Free Tier eligible)
  - For production: db.t3.medium or higher

#### Storage
| Setting | Value |
|---------|-------|
| Storage type | General Purpose SSD (gp2) |
| Allocated storage | **20 GB** (Free Tier allows up to 20 GB) |
| Enable storage autoscaling | ✅ Check this |
| Maximum storage threshold | 100 GB |

#### Connectivity
| Setting | Value |
|---------|-------|
| Compute resource | Don't connect to an EC2 |
| Network type | IPv4 |
| VPC | Default VPC |
| DB subnet group | Default |
| **Public access** | ✅ **Yes** (required to connect from your local machine) |
| VPC security group | **Create new** |
| New VPC security group name | `placement-db-sg` |
| Availability Zone | No preference |

#### Database Authentication
- ✅ **Password authentication**

#### Additional Configuration (expand this section!)
| Setting | Value |
|---------|-------|
| Initial database name | `placement_db` |
| Enable automated backups | ✅ Yes |
| Backup retention period | 7 days |
| Enable encryption | ✅ Yes |
| Enable Enhanced Monitoring | Unchecked (to stay in free tier) |

3. Click **"Create database"** — It takes **5-10 minutes** to provision.

### Step 2.3 — Get Your Endpoint
1. Once the status shows **"Available"**, click on your database instance
2. Under **"Connectivity & security"** tab, copy the **Endpoint** — it looks like:
   ```
   placement-system-db.xxxxxxxxxxxx.ap-south-1.rds.amazonaws.com
   ```
3. Note the **Port**: `5432`

---

## 3. Configure Security Group

Your database needs to allow incoming connections from your IP:

1. In the RDS dashboard, click on your database instance
2. Under **"Connectivity & security"**, click the **VPC security group** link (e.g., `placement-db-sg`)
3. Click the **Security Group ID**
4. Click **"Edit inbound rules"**
5. Add/modify the rule:

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| PostgreSQL | TCP | 5432 | My IP | Local development access |

   - **Source**: Select **"My IP"** — this auto-fills your current IP address
   - For production/deployment, you'll add the server's IP here too

6. Click **"Save rules"**

> 💡 **Tip**: If your IP changes (common with home internet), you'll need to update this rule. For development, you can temporarily set Source to `0.0.0.0/0` (anywhere), but **never do this in production**.

---

## 4. Connect Django to RDS

### Step 4.1 — Create `.env` File
Create a `.env` file in your project root (`d:\CODE THRIVE\placement_system\.env`):

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here

# AWS RDS PostgreSQL Database
DATABASE_URL=postgres://placementadmin:YOUR_PASSWORD@placement-system-db.xxxxxxxxxxxx.ap-south-1.rds.amazonaws.com:5432/placement_db

# AWS S3 Settings (optional, for media files)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=placement-system-bucket
AWS_S3_REGION_NAME=ap-south-1
```

Replace:
- `YOUR_PASSWORD` → Your RDS master password
- `xxxxxxxxxxxx` → Your actual RDS endpoint
- AWS keys → Your actual IAM credentials (see Section 6)

### Step 4.2 — Settings Are Already Updated!
The `settings.py` file has been updated (see changes below) to:
- Read `DATABASE_URL` from environment variables
- Fall back to SQLite for local development if no `DATABASE_URL` is set
- Support both local and cloud databases seamlessly

### Step 4.3 — Run Migrations on RDS
Once your `.env` file is configured with the correct `DATABASE_URL`:

```powershell
# Stop the current dev server first (Ctrl+C)

# Run migrations to create tables on RDS
.\venv\Scripts\python manage.py migrate

# Create a superuser on the new database
.\venv\Scripts\python manage.py createsuperuser

# Start the server
.\venv\Scripts\python manage.py runserver
```

---

## 5. Migrate Data from SQLite to RDS

### Option A: Using Django dumpdata/loaddata (Recommended)

#### Step 5.1 — Export Data from SQLite
Make sure your `.env` does NOT have `DATABASE_URL` set (or it points to SQLite):

```powershell
# Export all data from SQLite
.\venv\Scripts\python manage.py dumpdata --natural-foreign --natural-primary --exclude=contenttypes --exclude=auth.permission --exclude=admin.logentry --exclude=sessions.session --indent=2 > data_dump.json
```

#### Step 5.2 — Import Data to RDS
Now set your `DATABASE_URL` in `.env` to point to RDS, then:

```powershell
# First, run migrations on RDS to create the schema
.\venv\Scripts\python manage.py migrate

# Then load the data
.\venv\Scripts\python manage.py loaddata data_dump.json
```

### Option B: Using the Migration Script
A migration script (`migrate_to_rds.py`) has been created in your project. Run it:

```powershell
.\venv\Scripts\python migrate_to_rds.py
```

---

## 6. Set Up S3 for Media Files (Optional)

Since your app stores files (resumes, profile pictures, company logos), you should also use **AWS S3** for file storage in production.

### Step 6.1 — Create S3 Bucket
1. Go to **S3** in AWS Console (search "S3")
2. Click **"Create bucket"**
3. Settings:
   - Bucket name: `placement-system-media` (must be globally unique)
   - Region: Same as your RDS (e.g., ap-south-1)
   - Uncheck **"Block all public access"** (since you need to serve files)
   - Acknowledge the warning
4. Click **"Create bucket"**

### Step 6.2 — Create IAM User for S3 Access
1. Go to **IAM** in AWS Console
2. Click **Users** → **Create user**
3. Username: `placement-system-s3`
4. Click **Next** → **Attach policies directly**
5. Search and select: **AmazonS3FullAccess**
6. Click **Create user**
7. Click on the newly created user → **Security credentials** tab
8. **Create access key** → Choose **"Application running outside AWS"**
9. **Copy the Access Key ID and Secret Access Key** — save them securely!

### Step 6.3 — Update `.env`
```env
AWS_ACCESS_KEY_ID=AKIA...your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_STORAGE_BUCKET_NAME=placement-system-media
AWS_S3_REGION_NAME=ap-south-1
```

### Step 6.4 — Settings Are Updated!
The settings.py changes include S3 media storage configuration. When AWS credentials are detected, media files automatically go to S3.

---

## 7. Verify Everything Works

### Test Database Connection
```powershell
.\venv\Scripts\python manage.py dbshell
```
If you get a PostgreSQL prompt, you're connected! Type `\q` to exit.

### Test in Django Shell
```powershell
.\venv\Scripts\python manage.py shell
```
```python
from django.db import connection
print(connection.vendor)  # Should print 'postgresql'

from accounts.models import User
print(User.objects.count())  # Should show your user count
```

### Check in AWS Console
1. Go to **RDS** → Click your database instance
2. Check **"Monitoring"** tab to see connection activity
3. Check **"Logs & events"** for any issues

---

## 8. Cost Estimation

### Free Tier (First 12 months)
| Resource | Free Tier Limit | Your Usage |
|----------|----------------|------------|
| RDS db.t3.micro | 750 hrs/month | ~730 hrs (1 instance) |
| Storage | 20 GB | 20 GB |
| Backup | 20 GB | Auto |
| **Monthly Cost** | | **$0** |

### After Free Tier / Production (db.t3.micro)
| Resource | Cost |
|----------|------|
| RDS db.t3.micro (on-demand) | ~$12.41/month |
| 20 GB Storage | ~$2.30/month |
| Backup (20 GB) | ~$1.90/month |
| **Total** | **~$16.61/month** |

### Production (db.t3.medium)
| Resource | Cost |
|----------|------|
| RDS db.t3.medium | ~$49.64/month |
| 50 GB Storage | ~$5.75/month |
| **Total** | **~$55.39/month** |

> 💡 **Cost-Saving Tip**: Use **Reserved Instances** for a 1-year commitment to save up to 40%.

---

## Troubleshooting

### "Can't connect to RDS"
1. Check Security Group allows your IP on port 5432
2. Verify Public Access is set to "Yes"
3. Check if your IP changed (update Security Group)
4. Try: `ping your-rds-endpoint.amazonaws.com`

### "Authentication failed"
1. Double-check username and password in `.env`
2. Ensure no extra spaces in the DATABASE_URL
3. Try resetting the master password in RDS console

### "Relation does not exist"
1. Run `.\venv\Scripts\python manage.py migrate` first
2. Check if migrations were successful

### "Connection timed out"
1. Security Group is likely blocking your IP
2. Check if the RDS instance is in "Available" status
3. Verify the endpoint URL is correct

---

## Quick Reference

```
RDS Endpoint:    placement-system-db.xxxxxxxxxxxx.ap-south-1.rds.amazonaws.com
Port:            5432
Database Name:   placement_db
Master Username: placementadmin
Region:          ap-south-1 (Mumbai)
```

**Keep this document updated with your actual values after setup!**
