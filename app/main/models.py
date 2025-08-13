from django.db import models
from django.utils import timezone


class SiteVisit(models.Model):
    """Track visits to the website"""
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, null=True, blank=True)
    page_visited = models.CharField(max_length=200, default='/')
    
    class Meta:
        ordering = ['-timestamp']  # Most recent first
    
    def __str__(self):
        return f"Visit on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class VisitSummary(models.Model):
    """Store daily visit counts for performance"""
    date = models.DateField(unique=True)
    visit_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date}: {self.visit_count} visits"
