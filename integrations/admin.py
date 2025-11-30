from django.contrib import admin
from .models import ImportJob, ExportJob, Backup


@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'data_type', 'status', 'imported_records', 'failed_records', 'created_at']
    list_filter = ['source_type', 'data_type', 'data_format', 'status', 'created_at']
    search_fields = ['name', 'created_by__username', 'source_url']
    readonly_fields = ['created_at', 'updated_at', 'started_at', 'completed_at', 'duration']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'created_by')
        }),
        ('Source', {
            'fields': ('source_type', 'source_file', 'source_url')
        }),
        ('Data Type', {
            'fields': ('data_type', 'data_format')
        }),
        ('Configuration', {
            'fields': ('mapping', 'options'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'total_records', 'imported_records', 'failed_records', 'skipped_records')
        }),
        ('Errors', {
            'fields': ('error_log', 'error_file'),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'duration'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ExportJob)
class ExportJobAdmin(admin.ModelAdmin):
    list_display = ['name', 'data_type', 'export_format', 'status', 'total_records', 'file_size', 'created_at']
    list_filter = ['data_type', 'export_format', 'status', 'created_at']
    search_fields = ['name', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at', 'started_at', 'completed_at', 'duration']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'created_by')
        }),
        ('Export Configuration', {
            'fields': ('data_type', 'export_format', 'filters', 'options')
        }),
        ('Status', {
            'fields': ('status', 'file', 'total_records', 'file_size')
        }),
        ('Errors', {
            'fields': ('error_log',),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'duration', 'expires_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = ['name', 'backup_type', 'status', 'file_size_mb', 'is_restored', 'created_at']
    list_filter = ['backup_type', 'status', 'is_restored', 'created_at']
    search_fields = ['name', 'created_by__username', 'checksum']
    readonly_fields = ['created_at', 'updated_at', 'started_at', 'completed_at', 'duration', 'restored_at']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'backup_type', 'created_by')
        }),
        ('Content', {
            'fields': ('includes_database', 'includes_media', 'includes_settings')
        }),
        ('File', {
            'fields': ('file', 'file_size', 'checksum')
        }),
        ('Status', {
            'fields': ('status', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'duration', 'expires_at'),
            'classes': ('collapse',)
        }),
        ('Restoration', {
            'fields': ('is_restored', 'restored_at', 'restored_by'),
            'classes': ('collapse',)
        }),
        ('Errors', {
            'fields': ('error_log',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def file_size_mb(self, obj):
        """Display file size in MB"""
        return obj.file_size_mb
    file_size_mb.short_description = 'File Size (MB)'
