# Deployment Guide for Placement Readiness System

This guide outlines the steps to deploy the application to a production environment (e.g., AWS, Heroku, or DigitalOcean).

## 1. Prerequisites
- Python 3.10+
- PostgreSQL
- Nginx & Gunicorn
- AWS Account (for S3 and RDS)

## 2. Environment Setup
Create a `.env` file in the production server with the following:
```env
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=yourdomain.com,server_ip
DB_NAME=placement_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

## 3. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Run Migrations & Collect Static
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## 5. Configure Gunicorn
Create a gunicorn systemd service:
```bash
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/placement_system
ExecStart=/home/ubuntu/placement_system/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          placement_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

## 6. Configure Nginx
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/placement_system;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

## 7. AWS S3 for Media Files
In `settings.py`, configure `django-storages` to use AWS S3 for `MEDIA_ROOT`.

## 8. SSL with Certbot
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 9. Monitoring
Consider using Sentry for error tracking and Prometheus/Grafana for performance monitoring.
