# servicewatch_sa/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracking import views as tracking_views
from reports import views as reports_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tracking_views.dashboard, name='dashboard'),
    path('report/', reports_views.report_form, name='report_form'),
    
    # API Endpoints
    path('api/submit-report/', reports_views.submit_report, name='submit_report'),
    path('api/sync-offline/', reports_views.sync_offline_reports, name='sync_offline'),
    path('api/nearby-issues/', tracking_views.get_nearby_issues, name='nearby_issues'),
    path('api/all-issues/', tracking_views.get_all_issues, name='all_issues'),
    path('api/statistics/', tracking_views.get_statistics, name='statistics'),
    path('api/track/<str:reference>/', reports_views.track_issue, name='track_issue'),
    path('api/upvote/<str:reference>/', reports_views.upvote_issue, name='upvote_issue'),
    path('api/comment/<str:reference>/', reports_views.add_comment, name='add_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)