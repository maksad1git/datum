from django.contrib import admin
from .models import VisitType, Visit, Observation, VisitMedia, Sale


@admin.register(VisitType)
class VisitTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'type', 'is_active', 'requires_photo', 'requires_gps', 'created_at']
    list_filter = ['type', 'is_active', 'requires_photo', 'requires_signature', 'requires_gps', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    filter_horizontal = ['coefficients']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'description', 'type', 'is_active')
        }),
        ('Configuration', {
            'fields': ('form_template', 'coefficients')
        }),
        ('Requirements', {
            'fields': ('requires_photo', 'requires_signature', 'requires_gps')
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


class ObservationInline(admin.TabularInline):
    model = Observation
    extra = 0
    fields = ['coefficient', 'product', 'value_numeric', 'value_text', 'value_boolean']
    readonly_fields = []


class VisitMediaInline(admin.TabularInline):
    model = VisitMedia
    extra = 0
    fields = ['media_type', 'file', 'title']
    readonly_fields = []


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['outlet', 'visit_type', 'user', 'status', 'planned_date', 'start_date', 'created_at']
    list_filter = ['status', 'visit_type', 'created_at', 'planned_date']
    search_fields = ['outlet__name', 'user__username', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    inlines = [ObservationInline, VisitMediaInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('visit_type', 'outlet', 'user', 'status')
        }),
        ('Dates', {
            'fields': ('planned_date', 'start_date', 'end_date')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Data', {
            'fields': ('notes', 'signature', 'form_data'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ['visit', 'coefficient', 'product', 'value_numeric', 'value_boolean', 'created_at']
    list_filter = ['coefficient', 'created_at']
    search_fields = ['visit__outlet__name', 'coefficient__name', 'product__name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['visit', 'coefficient']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('visit', 'coefficient', 'product')
        }),
        ('Values', {
            'fields': ('value_numeric', 'value_text', 'value_boolean')
        }),
        ('Additional', {
            'fields': ('notes', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VisitMedia)
class VisitMediaAdmin(admin.ModelAdmin):
    list_display = ['visit', 'media_type', 'title', 'observation', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['visit__outlet__name', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['visit', 'created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('visit', 'observation', 'media_type')
        }),
        ('File', {
            'fields': ('file', 'thumbnail')
        }),
        ('Details', {
            'fields': ('title', 'description')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'exif_data'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'outlet', 'quantity', 'price', 'total_amount', 'sale_date', 'recorded_by']
    list_filter = ['sale_date', 'outlet__channel__district__city__region', 'recorded_at']
    search_fields = ['product__name', 'outlet__name']
    readonly_fields = ['total_amount', 'recorded_at']
    ordering = ['-sale_date']
    list_per_page = 50
    date_hierarchy = 'sale_date'

    fieldsets = (
        ('Basic Info', {
            'fields': ('outlet', 'product', 'sale_date')
        }),
        ('Sale Details', {
            'fields': ('quantity', 'price', 'total_amount')
        }),
        ('Metadata', {
            'fields': ('recorded_at', 'recorded_by'),
            'classes': ('collapse',)
        }),
    )
