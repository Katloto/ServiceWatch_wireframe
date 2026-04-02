# tracking/views.py
from django.shortcuts import render
from django.http import JsonResponse
from reports.models import IssueReport
from datetime import datetime, timedelta
import requests

def dashboard(request):
    """Main dashboard with map and stats"""
    return render(request, 'tracking/dashboard.html')

def get_nearby_issues(request):
    """API endpoint for getting issues within radius"""
    lat = float(request.GET.get('lat', -26.2041))
    lng = float(request.GET.get('lng', 28.0473))
    radius = float(request.GET.get('radius', 5))  # km
    
    # Simple bounding box filter (for demo)
    delta = radius / 111.0  # ~1 degree = 111km
    
    issues = IssueReport.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False,
        latitude__range=(lat - delta, lat + delta),
        longitude__range=(lng - delta, lng + delta)
    ).exclude(status='resolved').order_by('-created_at')[:50]
    
    data = [{
        'id': i.id,
        'reference': i.reference_number,
        'category': i.get_category_display(),
        'category_code': i.category,
        'status': i.get_status_display(),
        'status_code': i.status,
        'lat': float(i.latitude),
        'lng': float(i.longitude),
        'description': i.description[:100],
        'created_at': i.created_at.strftime('%Y-%m-%d %H:%M'),
        'upvotes': i.upvotes,
        'address': i.address
    } for i in issues]
    
    return JsonResponse({'success': True, 'issues': data})

def get_all_issues(request):
    issues = IssueReport.objects.all().order_by('-created_at')[:100]
    data = [{
        'reference': i.reference_number,
        'category': i.get_category_display(),
        'status': i.get_status_display(),
        'status_code': i.status,
        'description': i.description[:100],
        'created_at': i.created_at.strftime('%Y-%m-%d'),
        'upvotes': i.upvotes,
        'reporter': i.reporter_name
    } for i in issues]
    return JsonResponse({'success': True, 'issues': data})

def get_statistics(request):
    """Get dashboard statistics"""
    stats = {
        'total': IssueReport.objects.count(),
        'reported': IssueReport.objects.filter(status='reported').count(),
        'in_progress': IssueReport.objects.filter(status='in_progress').count(),
        'resolved': IssueReport.objects.filter(status='resolved').count(),
        'avg_resolution_time': 7.2,  # days (simulated)
    }
    
    # Issues by category
    category_stats = {}
    for cat, label in IssueReport.CATEGORY_CHOICES:
        count = IssueReport.objects.filter(category=cat).count()
        if count > 0:
            category_stats[label] = count
    
    stats['by_category'] = category_stats
    
    return JsonResponse({'success': True, 'stats': stats})