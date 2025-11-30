from django.contrib import admin
from .models import FormTemplate


@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'form_type', 'status', 'version', 'created_by', 'created_at']
    list_filter = ['form_type', 'status', 'created_at']
    search_fields = ['name', 'code', 'category']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    filter_horizontal = ['applies_to_channels']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'description', 'form_type', 'status')
        }),
        ('Configuration', {
            'fields': ('fields_schema', 'category', 'version', 'parent_version')
        }),
        ('Applicability', {
            'fields': ('applies_to_channels',)
        }),
        ('Creator', {
            'fields': ('created_by',)
        }),
        ('Settings', {
            'fields': ('settings',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
