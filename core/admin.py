from django.contrib import admin
from .models import SystemSettings, IntegrationSettings, SystemLog, AuditLog


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'currency', 'language', 'timezone', 'unit_system', 'default_country']
    list_filter = ['unit_system', 'language']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'logo', 'default_country')
        }),
        ('Localization', {
            'fields': ('currency', 'language', 'timezone', 'unit_system')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(IntegrationSettings)
class IntegrationSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_active', 'endpoint_url', 'created_at', 'updated_at']
    list_filter = ['type', 'is_active', 'created_at']
    search_fields = ['name', 'endpoint_url']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'type', 'is_active')
        }),
        ('Connection Settings', {
            'fields': ('endpoint_url', 'api_key', 'auth_params')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['level', 'action_type', 'user', 'ip_address', 'created_at']
    list_filter = ['level', 'action_type', 'created_at']
    search_fields = ['action_type', 'description', 'user__username', 'ip_address']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Log Info', {
            'fields': ('level', 'action_type', 'description')
        }),
        ('User Info', {
            'fields': ('user', 'ip_address', 'user_agent')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'table_name', 'record_id', 'user', 'timestamp', 'ip_address']
    list_filter = ['action', 'table_name', 'timestamp']
    search_fields = ['table_name', 'user__username', 'ip_address']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    list_per_page = 25
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('Action Info', {
            'fields': ('action', 'table_name', 'record_id')
        }),
        ('Changes', {
            'fields': ('old_value', 'new_value'),
            'classes': ('collapse',)
        }),
        ('User Info', {
            'fields': ('user', 'ip_address')
        }),
        ('Metadata', {
            'fields': ('timestamp',)
        }),
    )
