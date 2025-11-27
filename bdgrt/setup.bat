@echo off
REM ============================================
REM Birthday Greetings App Setup Script
REM ============================================

echo.
echo ========================================
echo  Birthday Greetings App Setup
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo ERROR: Virtual environment is not activated!
    echo Please activate your virtual environment first:
    echo   venv\Scripts\activate
    echo.
    pause
    exit /b 1
)

echo [1/8] Creating Django app 'greetings'...
python manage.py startapp greetings
echo     ✓ App created
echo.

echo [2/8] Creating directory structure...
mkdir greetings\templates\greetings 2>nul
mkdir greetings\static\greetings\css 2>nul
mkdir greetings\static\greetings\js 2>nul
mkdir greetings\static\greetings\images 2>nul
mkdir media 2>nul
mkdir static 2>nul
echo     ✓ Directories created
echo.

echo [3/8] Creating template files...
type nul > greetings\templates\greetings\base.html
type nul > greetings\templates\greetings\home.html
type nul > greetings\templates\greetings\login.html
type nul > greetings\templates\greetings\register.html
type nul > greetings\templates\greetings\dashboard.html
type nul > greetings\templates\greetings\create_greeting.html
type nul > greetings\templates\greetings\birthday.html
echo     ✓ Template files created
echo.

echo [4/8] Creating URL configuration...
type nul > greetings\urls.py
echo     ✓ URLs file created
echo.

echo [5/8] Creating requirements.txt...
(
echo Django^>=4.2
echo Pillow^>=10.0.0
echo mysqlclient^>=2.2.0
echo whitenoise^>=6.5.0
) > requirements.txt
echo     ✓ requirements.txt created
echo.

echo [6/8] Creating .gitignore...
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo.
echo # Virtual Environment
echo venv/
echo env/
echo ENV/
echo.
echo # Django
echo *.log
echo local_settings.py
echo db.sqlite3
echo db.sqlite3-journal
echo media/
echo staticfiles/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
) > .gitignore
echo     ✓ .gitignore created
echo.

echo [7/8] Creating README.md...
(
echo # Birthday Greetings App
echo.
echo A Django web application for creating and sharing personalized birthday greeting links.
echo.
echo ## Features
echo - User registration and authentication
echo - Create personalized birthday greetings
echo - Generate shareable unique URLs
echo - Beautiful animated birthday experience
echo - Dashboard to manage all greetings
echo.
echo ## Setup
echo 1. Activate virtual environment: `venv\Scripts\activate`
echo 2. Install dependencies: `pip install -r requirements.txt`
echo 3. Run migrations: `python manage.py migrate`
echo 4. Start server: `python manage.py runserver`
echo.
echo ## Project Structure
echo ```
echo bdgrt/
echo ├── birthday/              # Main Django project
echo ├── greetings/             # Greeting cards app
echo │   ├── templates/
echo │   ├── static/
echo │   ├── models.py
echo │   ├── views.py
echo │   └── urls.py
echo ├── media/                 # User uploads
echo ├── static/                # Static files
echo └── manage.py
echo ```
echo.
echo ## Usage
echo 1. Register/Login at http://127.0.0.1:8000/
echo 2. Create a new greeting from dashboard
echo 3. Share the generated link with recipient
echo 4. Recipient experiences beautiful animation
) > README.md
echo     ✓ README.md created
echo.

echo [8/8] Creating empty configuration marker files...
type nul > birthday\__init__.py
type nul > greetings\__init__.py
echo     ✓ Marker files created
echo.

echo ========================================
echo  Setup Complete! ✓
echo ========================================
echo.
echo Next Steps:
echo 1. Update birthday\settings.py (add 'greetings' to INSTALLED_APPS)
echo 2. Update birthday\urls.py (include greetings.urls)
echo 3. Update greetings\models.py (add User and Greeting models)
echo 4. Update greetings\views.py (add view functions)
echo 5. Update greetings\urls.py (add URL patterns)
echo 6. Add HTML content to template files
echo 7. Run: python manage.py makemigrations
echo 8. Run: python manage.py migrate
echo 9. Run: python manage.py runserver
echo.
echo Your project structure is ready!
echo.
echo Directory Structure Created:
echo.
echo bdgrt\
echo ├── birthday\
echo │   ├── __init__.py
echo │   ├── settings.py        ^<-- UPDATE THIS
echo │   ├── urls.py             ^<-- UPDATE THIS
echo │   ├── wsgi.py
echo │   └── asgi.py
echo ├── greetings\
echo │   ├── migrations\
echo │   ├── templates\
echo │   │   └── greetings\
echo │   │       ├── base.html           ^<-- ADD CODE
echo │   │       ├── home.html           ^<-- ADD CODE
echo │   │       ├── login.html          ^<-- ADD CODE
echo │   │       ├── register.html       ^<-- ADD CODE
echo │   │       ├── dashboard.html      ^<-- ADD CODE
echo │   │       ├── create_greeting.html ^<-- ADD CODE
echo │   │       └── birthday.html       ^<-- ADD CODE
echo │   ├── static\
echo │   │   └── greetings\
echo │   │       ├── css\
echo │   │       ├── js\
echo │   │       └── images\
echo │   ├── __init__.py
echo │   ├── admin.py
echo │   ├── apps.py
echo │   ├── models.py          ^<-- ADD CODE
echo │   ├── views.py           ^<-- ADD CODE
echo │   ├── urls.py            ^<-- ADD CODE
echo │   └── tests.py
echo ├── media\
echo ├── static\
echo ├── manage.py
echo ├── requirements.txt
echo ├── .gitignore
echo └── README.md
echo.
echo ========================================
pause
