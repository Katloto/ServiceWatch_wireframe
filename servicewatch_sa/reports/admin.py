# reports/admin.py
from django.contrib import admin
from .models import IssueReport, Comment, OfflineReport

@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'category', 'status', 'reporter_name', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['reference_number', 'reporter_name', 'reporter_email']
    readonly_fields = ['reference_number', 'created_at', 'updated_at']

admin.site.register(Comment)
admin.site.register(OfflineReport)