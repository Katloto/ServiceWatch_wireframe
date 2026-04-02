# reports/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from .models import IssueReport, Comment, OfflineReport
from .forms import IssueReportForm
import json
from datetime import datetime

def report_form(request):
    return render(request, 'reports/report_form.html')

@csrf_exempt
@require_http_methods(["POST"])
def submit_report(request):
    try:
        data = json.loads(request.body)
        
        report = IssueReport.objects.create(
            category=data.get('category'),
            description=data.get('description'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            address=data.get('address', ''),
            reporter_name=data.get('reporter_name'),
            reporter_email=data.get('reporter_email'),
            reporter_phone=data.get('reporter_phone'),
            created_offline=data.get('offline', False)
        )
        
        # Send confirmation email
        try:
            send_mail(
                f'ServiceWatch SA: Issue {report.reference_number}',
                f'Your report has been received. Track it at: /track/{report.reference_number}',
                'noreply@servicewatchsa.co.za',
                [report.reporter_email],
                fail_silently=True,
            )
        except:
            pass
        
        return JsonResponse({
            'success': True,
            'reference': report.reference_number,
            'message': 'Issue reported successfully!'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def sync_offline_reports(request):
    """Endpoint for syncing offline reports"""
    try:
        data = json.loads(request.body)
        reports = data.get('reports', [])
        
        created_refs = []
        for report_data in reports:
            report = IssueReport.objects.create(
                category=report_data.get('category'),
                description=report_data.get('description'),
                latitude=report_data.get('latitude'),
                longitude=report_data.get('longitude'),
                reporter_name=report_data.get('reporter_name'),
                reporter_email=report_data.get('reporter_email'),
                reporter_phone=report_data.get('reporter_phone'),
                created_offline=True
            )
            created_refs.append(report.reference_number)
        
        return JsonResponse({'success': True, 'synced': created_refs})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def track_issue(request, reference):
    issue = get_object_or_404(IssueReport, reference_number=reference)
    return JsonResponse({
        'reference': issue.reference_number,
        'status': issue.get_status_display(),
        'status_code': issue.status,
        'status_message': issue.status_message,
        'estimated_resolution': issue.estimated_resolution,
        'created_at': issue.created_at,
        'category': issue.get_category_display(),
        'upvotes': issue.upvotes,
        'comments': [{'user': c.user_name, 'text': c.text} for c in issue.comments.all()]
    })

@require_http_methods(["POST"])
def upvote_issue(request, reference):
    issue = get_object_or_404(IssueReport, reference_number=reference)
    issue.upvotes += 1
    issue.save()
    return JsonResponse({'success': True, 'upvotes': issue.upvotes})

@csrf_exempt
@require_http_methods(["POST"])
def add_comment(request, reference):
    issue = get_object_or_404(IssueReport, reference_number=reference)
    data = json.loads(request.body)
    Comment.objects.create(
        issue=issue,
        user_name=data.get('name'),
        text=data.get('comment')
    )
    issue.comments_count += 1
    issue.save()
    return JsonResponse({'success': True})