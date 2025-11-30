from django.contrib import admin
from .models import Dashboard, Report, ReportTemplate, FilterPreset, ForecastModel


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'dashboard_type', 'owner', 'is_public', 'is_active', 'created_at']
    list_filter = ['dashboard_type', 'is_public', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    filter_horizontal = ['shared_with']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'description', 'dashboard_type')
        }),
        ('Owner & Sharing', {
            'fields': ('owner', 'is_public', 'shared_with')
        }),
        ('Configuration', {
            'fields': ('widgets_config', 'default_filters', 'refresh_interval')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'template', 'created_by', 'status', 'format', 'date_from', 'date_to', 'created_at']
    list_filter = ['status', 'format', 'created_at', 'date_from']
    search_fields = ['name', 'created_by__username', 'template__name']
    readonly_fields = ['created_at', 'updated_at', 'generated_at', 'generation_time']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'template', 'created_by')
        }),
        ('Period', {
            'fields': ('date_from', 'date_to')
        }),
        ('Configuration', {
            'fields': ('format', 'filters', 'data'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'file')
        }),
        ('Generation Info', {
            'fields': ('generated_at', 'generation_time'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'report_type', 'category', 'is_active', 'created_by', 'created_at']
    list_filter = ['report_type', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['category', 'name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    filter_horizontal = ['metrics']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'description', 'report_type', 'category')
        }),
        ('Configuration', {
            'fields': ('config', 'sql_query', 'metrics')
        }),
        ('Creator', {
            'fields': ('created_by', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FilterPreset)
class FilterPresetAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'applies_to', 'is_public', 'created_at']
    list_filter = ['applies_to', 'is_public', 'created_at']
    search_fields = ['name', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['owner', 'name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'owner')
        }),
        ('Configuration', {
            'fields': ('applies_to', 'filters', 'is_public')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ForecastModel)
class ForecastModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'model_type', 'status', 'forecast_horizon', 'training_score', 'created_at']
    list_filter = ['model_type', 'status', 'created_at', 'trained_at']
    search_fields = ['name', 'code', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at', 'trained_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    filter_horizontal = ['metrics']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'description', 'model_type', 'status')
        }),
        ('Configuration', {
            'fields': ('metrics', 'parameters', 'forecast_horizon')
        }),
        ('Training', {
            'fields': ('training_data', 'training_score', 'trained_at'),
            'classes': ('collapse',)
        }),
        ('Creator', {
            'fields': ('created_by',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
