from django.urls import path
from . import views

app_name = 'grtcard'

urlpatterns = [
# Home & Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard & Management
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/theme/<str:theme>/', views.filter_by_theme, name='filter_by_theme'),
    
    # Greeting Management
    path('create/', views.create_greeting, name='create_greeting'),
    path('view/<uuid:unique_id>/', views.view_greeting, name='view_greeting'),
    path('edit/<uuid:unique_id>/', views.edit_greeting, name='edit_greeting'),
    path('update/<uuid:unique_id>/', views.update_greeting, name='update_greeting'),
    path('delete/<uuid:unique_id>/', views.delete_greeting, name='delete_greeting'),
    path('search/', views.search_greetings, name='search_greetings'),
    
    # API Endpoints
    path('api/theme/<str:theme>/', views.get_theme_details, name='get_theme_details'),
    path('api/stats/', views.get_dashboard_stats, name='dashboard_stats'),
    path('api/export/<uuid:unique_id>/', views.export_greeting, name='export_greeting'),
]