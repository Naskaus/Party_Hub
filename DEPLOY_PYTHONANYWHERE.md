# Party Hub - PythonAnywhere Deployment Guide

## Overview
Deploy the Marketing Event Planner on PythonAnywhere.com with SQLite (no PostgreSQL needed for MVP).

---

## Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Sign up for a **free** account (or paid for custom domain)
3. Note your username: `yourusername.pythonanywhere.com`

---

## Step 2: Clone Repository

Open a **Bash console** from the Dashboard:

```bash
# Clone from GitHub
cd ~
git clone https://github.com/Naskaus/Party_Hub.git

# Navigate to project
cd Party_Hub
```

---

## Step 3: Create Virtual Environment

```bash
# Create virtual environment (use Python 3.11+)
mkvirtualenv --python=/usr/bin/python3.11 partyhub

# Activate it
workon partyhub

# Install dependencies
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

Create `.env` file in project root:

```bash
nano ~/Party_Hub/.env
```

Add these settings:

```env
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this-!!!
ALLOWED_HOSTS=yourusername.pythonanywhere.com,localhost

# Database (SQLite is fine for MVP)
DATABASE_URL=sqlite:///db.sqlite3
```

> **Tip**: Generate a secret key with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

---

## Step 5: Database Setup

```bash
cd ~/Party_Hub
workon partyhub

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Enter: admin / your-email / your-password

# Collect static files
python manage.py collectstatic --noinput

# Optional: Load demo data
python seed_real_data.py
```

---

## Step 6: Configure Web App

1. Go to **Web** tab in PythonAnywhere Dashboard
2. Click **"Add a new web app"**
3. Select **"Manual configuration"** (NOT Django)
4. Choose **Python 3.11**

### 6.1 Source Code Path
```
/home/yourusername/Party_Hub
```

### 6.2 Virtualenv Path
```
/home/yourusername/.virtualenvs/partyhub
```

### 6.3 WSGI Configuration

Click on the WSGI config file link and **replace all content** with:

```python
import os
import sys
from pathlib import Path

# Add project to path
project_home = '/home/yourusername/Party_Hub'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Load environment variables from .env
from dotenv import load_dotenv
env_path = Path(project_home) / '.env'
load_dotenv(env_path)

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## Step 7: Static & Media Files

In the **Web** tab, add these static file mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/Party_Hub/staticfiles/` |
| `/media/` | `/home/yourusername/Party_Hub/media/` |

Make sure staticfiles directory exists:

```bash
mkdir -p ~/Party_Hub/staticfiles
mkdir -p ~/Party_Hub/media
```

---

## Step 8: Reload and Test

1. Click **"Reload"** button on Web tab
2. Visit `https://yourusername.pythonanywhere.com`
3. You should see the login page!

---

## Troubleshooting

### Check Error Logs
- Go to **Web** tab → **Error log**
- Check for import errors, missing env vars, etc.

### Common Issues

| Problem | Solution |
|---------|----------|
| "Module not found" | Check virtualenv path, run `pip install -r requirements.txt` |
| "DisallowedHost" | Add your domain to `ALLOWED_HOSTS` in `.env` |
| "Static files 404" | Run `python manage.py collectstatic` |
| "Database errors" | Run `python manage.py migrate` |

### Reload After Changes

After any code changes:
```bash
cd ~/Party_Hub
git pull origin main
workon partyhub
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click **"Reload"** on Web tab.

---

## Optional: PostgreSQL (Paid Plan)

For production with more users, upgrade to PostgreSQL:

1. PythonAnywhere creates DB for you (Postgres on paid plans)
2. Update `.env`:
```env
DATABASE_URL=postgres://username:password@yourusername-1234.postgres.pythonanywhere-services.com:5432/yourusername$dbname
```
3. Run migrations: `python manage.py migrate`

---

## Quick Checklist

- [ ] Account created on PythonAnywhere
- [ ] Repo cloned to `~/Party_Hub`
- [ ] Virtualenv created and activated
- [ ] `.env` file configured
- [ ] Database migrated
- [ ] Superuser created
- [ ] Static files collected
- [ ] WSGI configured
- [ ] Static/Media paths set
- [ ] App reloaded and working

---

**Your app will be live at:** `https://yourusername.pythonanywhere.com` 🎉
