# reports/models.py
from django.db import models
import uuid
from datetime import datetime, timedelta

class IssueReport(models.Model):
    CATEGORY_CHOICES = [
        ('water', '💧 Water Leak'),
        ('electricity', '⚡ Electricity Fault'),
        ('pothole', '🕳️ Pothole'),
        ('waste', '🗑️ Waste Collection'),
        ('sewage', '🚽 Sewage Issue'),
        ('streetlight', '💡 Streetlight Outage'),
    ]
    
    STATUS_CHOICES = [
        ('reported', '📋 Reported'),
        ('verified', '✅ Verified'),
        ('in_progress', '🔨 In Progress'),
        ('resolved', '🎉 Resolved'),
        ('rejected', '❌ Rejected'),
    ]
    
    reference_number = models.CharField(max_length=10, unique=True, editable=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    photo = models.ImageField(upload_to='reports/%Y/%m/%d/', null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    address = models.CharField(max_length=500, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    status_message = models.CharField(max_length=500, blank=True)
    estimated_resolution = models.DateTimeField(null=True, blank=True)
    
    reporter_name = models.CharField(max_length=100)
    reporter_email = models.EmailField()
    reporter_phone = models.CharField(max_length=15)
    
    upvotes = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    
    created_offline = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = f"SW{datetime.now().strftime('%y%m')}{uuid.uuid4().hex[:4].upper()}"
        if not self.estimated_resolution and self.status == 'in_progress':
            self.estimated_resolution = datetime.now() + timedelta(days=7)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.reference_number} - {self.get_category_display()}"

class Comment(models.Model):
    issue = models.ForeignKey(IssueReport, on_delete=models.CASCADE, related_name='comments')
    user_name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class OfflineReport(models.Model):
    """Queue for offline reports"""
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    synced = models.BooleanField(default=False)