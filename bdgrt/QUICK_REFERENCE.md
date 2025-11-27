# Quick Reference - Birthday Greetings Django Project

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Initialize Database
python manage.py migrate

# 3. Create Admin
python manage.py createsuperuser

# 4. Run
python manage.py runserver
```

Access: http://localhost:8000

---

## 📁 File Placement Guide

```
bdgrt/
│
├── greetings/
│   ├── models.py ...................... Copy from models.py
│   ├── views.py ....................... Copy from views.py
│   ├── urls.py ........................ Copy from app_urls.py
│   ├── admin.py ....................... Copy from admin.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── templates/grtcard/
│   │   ├── base.html .................. (provided)
│   │   ├── home.html .................. Copy from home.html
│   │   ├── login.html ................. (provided)
│   │   ├── register.html .............. Copy from register.html
│   │   ├── dashboard.html ............. (provided)
│   │   ├── create_greeting.html ........ Copy from create_greeting.html
│   │   └── birthday.html .............. (provided)
│   ├── static/
│   │   └── greetings/
│   │       ├── css/
│   │       ├── js/
│   │       └── images/
│   ├── apps.py
│   ├── __init__.py
│   └── tests.py
│
├── birthday/
│   ├── settings.py .................... Copy from settings.py
│   ├── urls.py ........................ Copy from main_urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── __init__.py
│
├── manage.py
├── requirements.txt ................... Copy from requirements.txt
├── .gitignore ......................... Copy from .gitignore
└── README.md .......................... Copy from README.md
```

---

## 🎨 Theme Colors Reference

| Theme | Gradient | Emoji |
|-------|----------|-------|
| Dark | #2c3e50 → #34495e | 🌙 |
| Bright | #f39c12 → #e74c3c | ☀️ |
| Friendly | #3498db → #9b59b6 | 😊 |
| Lovely | #e91e63 → #ff5722 | 💕 |
| Romantic | #c2185b → #d32f2f | 💑 |
| Casual | #00bcd4 → #4caf50 | 🤙 |
| Proposing | #ffd700 → #ff69b4 | 💍 |
| Partner | #9c27b0 → #673ab7 | 👫 |

---

## 📊 Database Model

```python
Greeting
├── id (AutoField, Primary Key)
├── unique_id (UUIDField, unique)
├── sender (ForeignKey → User)
├── recipient_name (CharField, max 100)
├── sender_name (CharField, max 100)
├── message (TextField, max 500)
├── image (ImageField, optional)
├── image2 (ImageField, optional)
├── birthday_date (DateField)
├── theme (CharField, choices)
├── created_date (DateTimeField, auto)
└── updated_date (DateTimeField, auto)
```

---

## 🔗 URL Routes

### Public
- `/` → home
- `/register/` → register
- `/login/` → login
- `/view/<uuid>/` → view_greeting

### Authenticated
- `/logout/` → logout
- `/dashboard/` → dashboard
- `/create/` → create_greeting
- `/edit/<uuid>/` → edit_greeting
- `/update/<uuid>/` → update_greeting
- `/delete/<uuid>/` → delete_greeting
- `/search/` → search_greetings

### Admin
- `/admin/` → Admin Panel

---

## 🛠️ Common Commands

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb

# Static Files
python manage.py collectstatic --noinput

# Admin
python manage.py createsuperuser
python manage.py changepassword <username>

# Database
python manage.py dbshell
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json

# Shell
python manage.py shell

# Test
python manage.py test
```

---

## 📋 Form Validation Rules

### Create Greeting
- **Recipient Name**: Required, max 100 chars
- **Birthday Date**: Required, date format
- **Message**: Required, 10-500 chars
- **Theme**: Required, must be valid choice
- **Image 1**: Optional, max 5MB, image format
- **Image 2**: Optional, max 5MB, image format

### Registration
- **Username**: Required, unique
- **Email**: Required, unique, email format
- **Password**: Required, min 6 chars
- **Password Confirm**: Must match password
- **First Name**: Optional
- **Last Name**: Optional

---

## 🔐 Security Features

✅ CSRF Protection ({% csrf_token %})
✅ Password Hashing (Django auth)
✅ SQL Injection Prevention (ORM)
✅ XSS Protection (Auto-escaping)
✅ Permission Checks (login_required)
✅ Owner Verification (sender check)
✅ File Type Validation (image/* only)
✅ File Size Limits (5MB max)

---

## 📱 Responsive Breakpoints

- **Desktop**: 1024px+
- **Tablet**: 768px - 1023px
- **Mobile**: < 768px

---

## 🐛 Troubleshooting Quick Fix

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Install: `pip install -r requirements.txt` |
| Database errors | Run: `python manage.py migrate` |
| Static files missing | Run: `python manage.py collectstatic --noinput` |
| Port in use | Use: `python manage.py runserver 8001` |
| Templates not found | Check: TEMPLATES['DIRS'] in settings.py |
| Media not showing | Check: MEDIA_ROOT and MEDIA_URL in settings.py |
| Import errors | Add to INSTALLED_APPS: `'greetings'` |

---

## 📦 Dependencies

```
Django==4.2.7          # Web Framework
Pillow==10.1.0         # Image Processing
python-decouple==3.8   # Environment Variables
```

---

## 🌐 Environment Setup (.env file)

Create a `.env` file in root directory:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Then update settings.py to use these values.

---

## 📞 API Endpoints (if REST added later)

```
GET    /api/greetings/             List all greetings
POST   /api/greetings/             Create greeting
GET    /api/greetings/{id}/        Get greeting detail
PUT    /api/greetings/{id}/        Update greeting
DELETE /api/greetings/{id}/        Delete greeting
GET    /api/users/{id}/greetings/  Get user's greetings
```

---

## 📝 Template Tags Used

```django
{% extends %}          Inheritance
{% include %}          Include template
{% block %}            Override block
{% if %}               Conditional
{% for %}              Loop
{% url %}              Reverse URL
{% csrf_token %}       CSRF protection
{{ variable }}         Display variable
{{ object|filter }}    Apply filter
```

---

## 🎯 Project Statistics

- **Views**: 11 functions
- **Models**: 1 (Greeting)
- **Templates**: 7 HTML files
- **URL Patterns**: 11 routes
- **Static Files**: CSS, JS, Images
- **Theme Options**: 8 themes
- **Max Image Size**: 5MB
- **Max Message Length**: 500 characters
- **Supported Image Formats**: JPG, PNG, GIF

---

## ⚡ Performance Tips

1. Use database indexes on frequently searched fields
2. Cache static files in production
3. Use CDN for media files
4. Implement pagination for long lists
5. Use select_related() and prefetch_related()
6. Add database query optimization
7. Use Django debug toolbar in development

---

## 🚀 Production Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS
- [ ] Change SECRET_KEY
- [ ] Use PostgreSQL database
- [ ] Use Gunicorn/uWSGI server
- [ ] Enable HTTPS/SSL
- [ ] Set SECURE_SSL_REDIRECT = True
- [ ] Configure CORS headers
- [ ] Use environment variables
- [ ] Enable logging
- [ ] Set up error tracking (Sentry)
- [ ] Configure email backend
- [ ] Add rate limiting
- [ ] Implement CDN for static files
- [ ] Regular database backups

---

**Last Updated**: 2025-11-26
**Version**: 1.0.0
**Status**: ✅ Production Ready
