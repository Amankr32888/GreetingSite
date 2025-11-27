from django.contrib import admin

# Register your models here.
from .models import Greeting

@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ('recipient_name', 'sender_name', 'theme', 'birthday_date', 'created_date')
    list_filter = ('theme', 'created_date', 'birthday_date')
    search_fields = ('recipient_name', 'sender_name', 'message', 'unique_id')
    readonly_fields = ('unique_id', 'created_date', 'updated_date')
    
    fieldsets = (
        ('Greeting Information', {
            'fields': ('unique_id', 'sender', 'recipient_name', 'sender_name')
        }),
        ('Message Details', {
            'fields': ('message', 'theme')
        }),
        ('Images', {
            'fields': ('image', 'image2')
        }),
        ('Dates', {
            'fields': ('birthday_date', 'created_date', 'updated_date')
        }),
    )

    def has_add_permission(self, request):
        return False