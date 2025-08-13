from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Count
from .models import SiteVisit, VisitSummary
import datetime


def get_client_ip(request):
    """Get the client's IP address from the request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def track_visit(request, page='/'):
    """Track a visit to the site - only count unique IPs per day"""
    try:
        ip_address = get_client_ip(request)
        today = timezone.now().date()
        
        # Check if this IP has already visited today
        is_first_visit_today = not SiteVisit.objects.filter(
            ip_address=ip_address,
            timestamp__date=today
        ).exists()
        
        # Always record the visit for detailed logging
        SiteVisit.objects.create(
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            page_visited=page
        )
        
        # Only increment counter if this is the first visit from this IP today
        if is_first_visit_today:
            summary, created = VisitSummary.objects.get_or_create(
                date=today,
                defaults={'visit_count': 0}
            )
            summary.visit_count += 1
            summary.save()
        
    except Exception as e:
        # Don't break the site if visit tracking fails
        print(f"Visit tracking error: {e}")


def get_visit_stats():
    """Get basic visit statistics - counting unique IP addresses"""
    # Total unique visitors (unique IP addresses)
    total_unique_visitors = SiteVisit.objects.values('ip_address').distinct().count()
    
    today = timezone.now().date()
    # Today's unique visitors
    today_unique_visitors = SiteVisit.objects.filter(
        timestamp__date=today
    ).values('ip_address').distinct().count()
    
    # Get last 7 days unique visitors
    week_ago = today - datetime.timedelta(days=7)
    week_unique_visitors = SiteVisit.objects.filter(
        timestamp__date__gte=week_ago
    ).values('ip_address').distinct().count()
    
    # Total page views (all visits)
    total_page_views = SiteVisit.objects.count()
    
    return {
        'total_visits': total_unique_visitors,  # Now represents unique visitors
        'today_visits': today_unique_visitors,
        'week_visits': week_unique_visitors,
        'total_page_views': total_page_views,  # All visits for reference
    }


def welcome(request):
    # Track the visit
    track_visit(request, '/')
    
    # Simple welcome page without statistics
    return render(request, "home/welcome.html")


def statistics(request):
    # Track the visit
    track_visit(request, '/statistics')
    
    # Get visit statistics
    stats = get_visit_stats()
    
    # Statistics page
    return render(request, "home/statistics.html", {'stats': stats})


def about(request):
    track_visit(request, '/about')
    return render(request, "home/about.html")
