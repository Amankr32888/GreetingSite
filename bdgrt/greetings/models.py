from django.db import models
from django.contrib.auth.models import User
import uuid

class Greeting(models.Model):
    THEME_CHOICES = [
        ('dark', 'Dark 🌙'),
        ('bright', 'Bright ☀️'),
        ('friendly', 'Friendly 😊'),
        ('lovely', 'Lovely 💕'),
        ('romantic', 'Romantic 💑'),
        ('casual', 'Casual 🤙'),
        ('proposing', 'Proposing 💍'),
        ('partner', 'Partner 👫'),
    ]

    # Primary Fields
    id = models.AutoField(primary_key=True)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_greetings')
    
    # Recipient Information
    recipient_name = models.CharField(max_length=100)
    sender_name = models.CharField(max_length=100)
    birthday_date = models.DateField()
    
    # Message Content
    message = models.TextField(max_length=500)
    
    # Media (Optional)
    image = models.ImageField(upload_to='greetings/images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='greetings/images/', null=True, blank=True)
    
    # Theme Selection
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='lovely')
    
    # Timestamps
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Card Status
    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['sender', '-created_date']),
            models.Index(fields=['unique_id']),
            models.Index(fields=['theme']),
        ]
    
    def __str__(self):
        return f"Birthday greeting for {self.recipient_name} by {self.sender_name}"
    
    def get_absolute_url(self):
        return f"/greetings/view/{self.unique_id}/"
    
    def increment_views(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])