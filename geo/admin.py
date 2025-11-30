from django.contrib import admin
from .models import (
    GlobalMarket, Country, Region, Channel, Outlet,
    FootfallCounter, OutletInventory, Display, DisplayInventory
)


@admin.register(GlobalMarket)
class GlobalMarketAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'currency', 'data_type', 'unit_weight', 'created_at']
    list_filter = ['data_type', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'description')
        }),
        ('Settings', {
            'fields': ('currency', 'unit_weight', 'data_type', 'settings')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'iso_code', 'global_market', 'currency', 'created_at']
    list_filter = ['global_market', 'created_at']
    search_fields = ['name', 'code', 'iso_code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'iso_code', 'global_market')
        }),
        ('Settings', {
            'fields': ('currency', 'flag_image', 'settings')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country', 'data_type', 'created_at']
    list_filter = ['country', 'data_type', 'created_at']
    search_fields = ['name', 'code', 'country__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['country', 'name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'country')
        }),
        ('Settings', {
            'fields': ('data_type', 'geo_polygon', 'settings')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'region', 'type', 'created_at']
    list_filter = ['type', 'region__country', 'created_at']
    search_fields = ['name', 'code', 'region__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['region', 'name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'region', 'type')
        }),
        ('Details', {
            'fields': ('description', 'settings')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'channel', 'status', 'contact_phone', 'created_at']
    list_filter = ['status', 'channel__region__country', 'created_at']
    search_fields = ['name', 'code', 'address', 'contact_person', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['channel', 'name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'channel', 'status')
        }),
        ('Contact Info', {
            'fields': ('address', 'contact_phone', 'contact_person')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'photo')
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


@admin.register(FootfallCounter)
class FootfallCounterAdmin(admin.ModelAdmin):
    list_display = ['outlet', 'timestamp', 'count', 'counted_by']
    list_filter = ['outlet__channel__region', 'timestamp']
    search_fields = ['outlet__name']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    list_per_page = 50
    date_hierarchy = 'timestamp'


@admin.register(OutletInventory)
class OutletInventoryAdmin(admin.ModelAdmin):
    list_display = ['outlet', 'product', 'quantity', 'last_updated', 'updated_by']
    list_filter = ['outlet__channel__region', 'outlet__channel', 'last_updated']
    search_fields = ['outlet__name', 'product__name']
    readonly_fields = ['last_updated']
    ordering = ['outlet', 'product']
    list_per_page = 50


@admin.register(Display)
class DisplayAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_type', 'outlet', 'location', 'is_active']
    list_filter = ['display_type', 'outlet__channel__region', 'is_active']
    search_fields = ['name', 'outlet__name', 'location']
    ordering = ['outlet', 'name']
    list_per_page = 50


@admin.register(DisplayInventory)
class DisplayInventoryAdmin(admin.ModelAdmin):
    list_display = ['display', 'product', 'quantity', 'position', 'last_updated']
    list_filter = ['display__outlet__channel__region', 'last_updated']
    search_fields = ['display__name', 'product__name']
    readonly_fields = ['last_updated']
    ordering = ['display', 'product']
    list_per_page = 50
