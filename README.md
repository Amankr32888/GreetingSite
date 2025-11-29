# Birthday Greetings App

A Django web application for creating and sharing personalized birthday greeting links.

## Features
- User registration and authentication
- Create personalized birthday greetings
- Generate shareable unique URLs
- Beautiful animated birthday experience
- Dashboard to manage all greetings

## Setup
1. Activate virtual environment: `venv\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## Project Structure
```
bdgrt/
├── birthday/              # Main Django project
├── greetings/             # Greeting cards app
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── media/                 # User uploads
├── static/                # Static files
└── manage.py
```

## Usage
1. Register/Login at http://127.0.0.1:8000/
2. Create a new greeting from dashboard
3. Share the generated link with recipient
4. Recipient experiences beautiful animation
