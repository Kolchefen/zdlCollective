from django.contrib import admin
from .models import SiteVisit, VisitSummary


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'ip_address', 'page_visited']
    list_filter = ['timestamp', 'page_visited']
    readonly_fields = ['timestamp', 'ip_address', 'user_agent', 'page_visited']
    ordering = ['-timestamp']


@admin.register(VisitSummary)
class VisitSummaryAdmin(admin.ModelAdmin):
    list_display = ['date', 'visit_count']
    list_filter = ['date']
    ordering = ['-date']
