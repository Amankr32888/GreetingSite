from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden , JsonResponse
from .models import Greeting
from django.db.models import Q
from django.core.paginator import Paginator
import json
from django.db import models

import mimetypes

def home(request):
    greetings = Greeting.objects.all()[:6]
    context = {
        'greetings': greetings,
        'total_greetings': Greeting.objects.count(),
        'total_users': User.objects.count(),
    }
    return render(request, 'grtcard/home.html', context)

@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect('grtcard:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('grtcard:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('grtcard:register')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
            return redirect('grtcard:register')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters!')
            return redirect('grtcard:register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('grtcard:login')

    return render(request, 'grtcard/register.html')

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('grtcard:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('grtcard:dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('grtcard:login')

    return render(request, 'grtcard/login.html')

@login_required(login_url='grtcard:login')
@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('grtcard:home')

# @login_required(login_url='grtcard:login')
# @require_http_methods(["GET"])
# def dashboard(request):
#     greetings = Greeting.objects.filter(sender=request.user)
#     context = {
#         'greetings': greetings,
#         'total_greetings': greetings.count(),
#     }
#     return render(request, 'grtcard/dashboard.html', context)

# ADD THIS FUNCTION - View Greeting by Theme
# ============================================================================

@require_http_methods(["GET"])
def view_greeting(request, unique_id):
    """
    Display greeting card with theme-specific template
    - Increments view count
    - Loads theme-specific styling
    """
    try:
        greeting = get_object_or_404(Greeting, unique_id=unique_id, is_published=True)
        greeting.increment_views()
        
        # Theme-specific context
        theme_context = {
            'greeting': greeting,
            'theme': greeting.theme,
            'theme_name': dict(greeting.THEME_CHOICES).get(greeting.theme, 'Default'),
        }
        
        # Use generic theme template that handles all themes
        return render(request, 'grtcard/birthday_theme.html', theme_context)
    
    except Greeting.DoesNotExist:
        messages.error(request, 'Greeting card not found or has been removed.')
        return redirect('grtcard:home')


# ============================================================================
# UPDATEd - Dashboard with Enhanced Card Display
# ============================================================================

@login_required(login_url='grtcard:login')
@require_http_methods(["GET"])
def dashboard(request):
    """
    User dashboard showing all their created greetings
    - Display greeting cards with theme preview
    - Show card details (recipient, date created, views)
    - Options to view, edit, delete cards
    """
    greetings = Greeting.objects.filter(sender=request.user).order_by('-created_date')
    
    # Pagination
    paginator = Paginator(greetings, 6)
    page_number = request.GET.get('page')
    greetings_page = paginator.get_page(page_number)
    
    # Statistics
    total_greetings = greetings.count()
    total_views = greetings.aggregate(total=models.Sum('view_count'))['total'] or 0
    
    context = {
        'greetings': greetings_page,
        'total_greetings': total_greetings,
        'total_views': total_views,
        'themes': Greeting.THEME_CHOICES,
    }
    
    return render(request, 'grtcard/dashboard.html', context)


# ============================================================================
#  Delete Greeting with CSRF

@login_required(login_url='grtcard:login')
@require_http_methods(["POST"])
def delete_greeting(request, unique_id):
    """
    Delete greeting card - Only owner can delete
    """
    greeting = get_object_or_404(Greeting, unique_id=unique_id)
    
    # Check if user is the owner
    if greeting.sender != request.user:
        messages.error(request, 'You cannot delete this greeting.')
        return redirect('grtcard:dashboard')
    
    # Store recipient name for message
    recipient_name = greeting.recipient_name
    
    # Delete images if they exist
    if greeting.image:
        greeting.image.delete()
    if greeting.image2:
        greeting.image2.delete()
    
    greeting.delete()
    messages.success(request, f'Greeting for {recipient_name} has been deleted successfully.')
    return redirect('grtcard:dashboard')


# ============================================================================
#  Get Theme Details (AJAX)


@require_http_methods(["GET"])
def get_theme_details(request, theme):
    """
    Return theme details for preview (AJAX endpoint)
    """
    THEME_DETAILS = {
        'dark': {
            'name': 'Dark 🌙',
            'description': 'Elegant dark theme',
            'colors': ['#2c3e50', '#34495e'],
            'icon': '🌙'
        },
        'bright': {
            'name': 'Bright ☀️',
            'description': 'Vibrant and energetic',
            'colors': ['#f39c12', '#e74c3c'],
            'icon': '☀️'
        },
        'friendly': {
            'name': 'Friendly 😊',
            'description': 'Warm and friendly',
            'colors': ['#3498db', '#9b59b6'],
            'icon': '😊'
        },
        'lovely': {
            'name': 'Lovely 💕',
            'description': 'Sweet and cute',
            'colors': ['#e91e63', '#ff5722'],
            'icon': '💕'
        },
        'romantic': {
            'name': 'Romantic 💑',
            'description': 'Deep and romantic',
            'colors': ['#c2185b', '#d32f2f'],
            'icon': '💑'
        },
        'casual': {
            'name': 'Casual 🤙',
            'description': 'Cool and casual',
            'colors': ['#00bcd4', '#4caf50'],
            'icon': '🤙'
        },
        'proposing': {
            'name': 'Proposing 💍',
            'description': 'Special and magical',
            'colors': ['#ffd700', '#ff69b4'],
            'icon': '💍'
        },
        'partner': {
            'name': 'Partner 👫',
            'description': 'For your special partner',
            'colors': ['#9c27b0', '#673ab7'],
            'icon': '👫'
        },
    }
    
    theme_data = THEME_DETAILS.get(theme)
    if not theme_data:
        return JsonResponse({'error': 'Theme not found'}, status=404)
    
    return JsonResponse(theme_data)


# ============================================================================
# ADD THIS FUNCTION - Filter Greetings by Theme
# ============================================================================

@login_required(login_url='grtcard:login')
@require_http_methods(["GET"])
def filter_by_theme(request, theme):
    """
    Display user's greetings filtered by theme
    """
    valid_themes = [t[0] for t in Greeting.THEME_CHOICES]
    
    if theme not in valid_themes:
        messages.error(request, 'Invalid theme.')
        return redirect('grtcard:dashboard')
    
    greetings = Greeting.objects.filter(
        sender=request.user,
        theme=theme
    ).order_by('-created_date')
    
    paginator = Paginator(greetings, 6)
    page_number = request.GET.get('page')
    greetings_page = paginator.get_page(page_number)
    
    context = {
        'greetings': greetings_page,
        'current_theme': theme,
        'theme_name': dict(Greeting.THEME_CHOICES).get(theme),
        'themes': Greeting.THEME_CHOICES,
    }
    
    return render(request, 'grtcard/dashboard_filtered.html', context)


# ============================================================================
# ADD THIS FUNCTION - Export Greeting (Download as PDF - Optional)
# ============================================================================

@login_required(login_url='grtcard:login')
@require_http_methods(["GET"])
def export_greeting(request, unique_id):
    """
    Export greeting card as text/data
    - Only owner can export
    """
    greeting = get_object_or_404(Greeting, unique_id=unique_id)
    
    if greeting.sender != request.user:
        return HttpResponseForbidden('You do not have permission to export this greeting.')
    
    export_data = {
        'recipient_name': greeting.recipient_name,
        'sender_name': greeting.sender_name,
        'birthday_date': str(greeting.birthday_date),
        'message': greeting.message,
        'theme': greeting.theme,
        'created_date': str(greeting.created_date),
        'link': request.build_absolute_uri(f'/greetings/view/{greeting.unique_id}/'),
    }
    
    return JsonResponse(export_data)


# ============================================================================
#  Create Greeting (Add theme preview)
# ============================================================================

# In your existing create_greeting view, add:

@login_required(login_url='grtcard:login')
@require_http_methods(["GET", "POST"])
def create_greeting(request):
    """
    Create greeting card with theme selection and preview
    """
    if request.method == 'POST':
        recipient_name = request.POST.get('recipient_name', '').strip()
        birthday_date = request.POST.get('birthday_date', '').strip()
        message = request.POST.get('message', '').strip()
        theme = request.POST.get('theme', '').strip()
        image = request.FILES.get('image')
        image2 = request.FILES.get('image2')
        
        # Validation
        errors = {}
        
        if not recipient_name or len(recipient_name) < 2:
            errors['recipient_name'] = 'Please enter a valid recipient name.'
        
        if not birthday_date:
            errors['birthday_date'] = 'Please select a birthday date.'
        
        if not message or len(message) < 10:
            errors['message'] = 'Message must be at least 10 characters long.'
        
        if not message or len(message) > 500:
            errors['message'] = 'Message cannot exceed 500 characters.'
        
        if not theme or theme not in [t[0] for t in Greeting.THEME_CHOICES]:
            errors['theme'] = 'Please select a valid theme.'
        
        # Validate image sizes
        if image and image.size > 5 * 1024 * 1024:
            errors['image'] = 'Image 1 must be less than 5MB.'
        
        if image2 and image2.size > 5 * 1024 * 1024:
            errors['image2'] = 'Image 2 must be less than 5MB.'
        
        if errors:
            context = {
                'form_errors': errors,
                'form_data': request.POST,
                'themes': Greeting.THEME_CHOICES,
            }
            return render(request, 'grtcard/create_greeting.html', context)
        
        # Create greeting
        greeting = Greeting(
            sender=request.user,
            recipient_name=recipient_name,
            sender_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            birthday_date=birthday_date,
            message=message,
            theme=theme,
            image=image,
            image2=image2,
            is_published=True,
        )
        greeting.save()
        
        messages.success(request, f'Birthday greeting for {recipient_name} created successfully! 🎉')
        return redirect('grtcard:dashboard')
    
    # GET request
    context = {
        'themes': Greeting.THEME_CHOICES,
    }
    
    return render(request, 'grtcard/create_greeting.html', context)


# ============================================================================
# ADD STATISTICS FUNCTION (Dashboard Enhancement)
# ============================================================================

@login_required(login_url='grtcard:login')
def get_dashboard_stats(request):
    """
    Get dashboard statistics as JSON (for AJAX updates)
    """
    greetings = Greeting.objects.filter(sender=request.user)
    
    stats = {
        'total_greetings': greetings.count(),
        'total_views': sum(g.view_count for g in greetings),
        'themes_used': greetings.values('theme').distinct().count(),
        'theme_breakdown': dict(
            greetings.values('theme').annotate(count=models.Count('id')).values_list('theme', 'count')
        ),
    }
    
    return JsonResponse(stats)


# ============================================================================

# @login_required(login_url='grtcard:login')
# @require_http_methods(["GET", "POST"])
# def create_greeting(request):
#     if request.method == 'POST':
#         recipient_name = request.POST.get('recipient_name', '').strip()
#         birthday_date = request.POST.get('birthday_date')
#         message = request.POST.get('message', '').strip()
#         theme = request.POST.get('theme', 'lovely')
#         image = request.FILES.get('image')
#         image2 = request.FILES.get('image2')

#         if not recipient_name:
#             messages.error(request, 'Please enter recipient name!')
#             return redirect('grtcard:create_greeting')

#         if not message or len(message) < 10:
#             messages.error(request, 'Message must be at least 10 characters!')
#             return redirect('grtcard:create_greeting')

#         if not birthday_date:
#             messages.error(request, 'Please select birthday date!')
#             return redirect('grtcard:create_greeting')

#         if theme not in dict(Greeting.THEME_CHOICES):
#             messages.error(request, 'Invalid theme selected!')
#             return redirect('grtcard:create_greeting')

#         greeting = Greeting.objects.create(
#             sender=request.user,
#             recipient_name=recipient_name,
#             sender_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
#             message=message,
#             birthday_date=birthday_date,
#             theme=theme,
#             image=image,
#             image2=image2
#         )

#         messages.success(request, 'Birthday greeting created successfully!')
#         return redirect('grtcard:view_greeting', unique_id=greeting.unique_id)

#     return render(request, 'grtcard/create_greeting.html')

@require_http_methods(["GET"])
def view_greeting(request, unique_id):
    greeting = get_object_or_404(Greeting, unique_id=unique_id)
    context = {
        'greeting': greeting,
        'theme': greeting.theme,
    }
    return render(request, 'grtcard/birthday.html', context)

@login_required(login_url='grtcard:login')
@require_http_methods(["POST"])
def delete_greeting(request, unique_id):
    greeting = get_object_or_404(Greeting, unique_id=unique_id)
    
    if greeting.sender != request.user:
        messages.error(request, 'You cannot delete this greeting!')
        return redirect('grtcard:dashboard')

    greeting.delete()
    messages.success(request, 'Greeting deleted successfully!')
    return redirect('grtcard:dashboard')

@login_required(login_url='grtcard:login')
@require_http_methods(["GET"])
def edit_greeting(request, unique_id):
    greeting = get_object_or_404(Greeting, unique_id=unique_id)
    
    if greeting.sender != request.user:
        messages.error(request, 'You cannot edit this greeting!')
        return redirect('grtcard:dashboard')

    context = {
        'greeting': greeting,
    }
    return render(request, 'grtcard/edit_greeting.html', context)

@login_required(login_url='grtcard:login')
@require_http_methods(["POST"])
def update_greeting(request, unique_id):
    greeting = get_object_or_404(Greeting, unique_id=unique_id)
    
    if greeting.sender != request.user:
        messages.error(request, 'You cannot update this greeting!')
        return redirect('grtcard:dashboard')

    recipient_name = request.POST.get('recipient_name', '').strip()
    birthday_date = request.POST.get('birthday_date')
    message = request.POST.get('message', '').strip()
    theme = request.POST.get('theme', greeting.theme)

    if not recipient_name:
        messages.error(request, 'Please enter recipient name!')
        return redirect('grtcard:edit_greeting', unique_id=unique_id)

    if not message or len(message) < 10:
        messages.error(request, 'Message must be at least 10 characters!')
        return redirect('grtcard:edit_greeting', unique_id=unique_id)

    if not birthday_date:
        messages.error(request, 'Please select birthday date!')
        return redirect('grtcard:edit_greeting', unique_id=unique_id)

    greeting.recipient_name = recipient_name
    greeting.birthday_date = birthday_date
    greeting.message = message
    greeting.theme = theme

    if 'image' in request.FILES:
        greeting.image = request.FILES['image']

    if 'image2' in request.FILES:
        greeting.image2 = request.FILES['image2']

    greeting.save()
    messages.success(request, 'Greeting updated successfully!')
    return redirect('grtcard:view_greeting', unique_id=unique_id)

@require_http_methods(["GET"])
def search_greetings(request):
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        messages.warning(request, 'Search query must be at least 2 characters!')
        return render(request, 'grtcard/search.html', {'greetings': []})

    greetings = Greeting.objects.filter(
        Q(recipient_name__icontains=query) |
        Q(sender_name__icontains=query) |
        Q(message__icontains=query)
    )

    context = {
        'greetings': greetings,
        'query': query,
        'count': greetings.count(),
    }
    return render(request, 'grtcard/search.html', context)
