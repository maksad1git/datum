from django.contrib import admin
from .models import Coefficient, Metric, Formula, Rule


@admin.register(Coefficient)
class CoefficientAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'data_type', 'value_type', 'unit', 'is_active', 'created_at']
    list_filter = ['data_type', 'value_type', 'is_active', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'description', 'is_active')
        }),
        ('Type Settings', {
            'fields': ('data_type', 'value_type', 'unit')
        }),
        ('Applicability', {
            'fields': ('applies_to_outlet', 'applies_to_channel', 'applies_to_region',
                      'applies_to_country', 'applies_to_global')
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


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'formula', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['category', 'name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    filter_horizontal = ['coefficients']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'description', 'is_active')
        }),
        ('Configuration', {
            'fields': ('category', 'formula', 'coefficients')
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


@admin.register(Formula)
class FormulaAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'result_type', 'result_unit', 'is_active', 'created_at']
    list_filter = ['result_type', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'expression']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    filter_horizontal = ['coefficients']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'description', 'is_active')
        }),
        ('Formula', {
            'fields': ('expression', 'coefficients')
        }),
        ('Result', {
            'fields': ('result_type', 'result_unit')
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


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'rule_type', 'aggregation_method', 'is_active', 'created_at']
    list_filter = ['rule_type', 'aggregation_method', 'is_active', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['rule_type', 'name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    filter_horizontal = ['applies_to']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'description', 'is_active')
        }),
        ('Configuration', {
            'fields': ('rule_type', 'aggregation_method', 'applies_to')
        }),
        ('Parameters', {
            'fields': ('parameters',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
