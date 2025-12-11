"""
API URL Configuration for AJAX endpoints
"""
from django.urls import path
from . import ajax_views

app_name = 'api'

urlpatterns = [
    # ============================================================================
    # GEO CASCADE: GlobalMarket → Country → Region → City → District → Channel → Outlet
    # ============================================================================
    path('ajax/countries/', ajax_views.ajax_countries_by_globalmarket, name='ajax_countries_by_globalmarket'),
    path('ajax/regions/', ajax_views.ajax_regions_by_country, name='ajax_regions_by_country'),
    path('ajax/cities/', ajax_views.ajax_cities_by_region, name='ajax_cities_by_region'),
    path('ajax/districts/', ajax_views.ajax_districts_by_city, name='ajax_districts_by_city'),
    path('ajax/channels/', ajax_views.ajax_channels_by_district, name='ajax_channels_by_district'),
    path('ajax/outlets/', ajax_views.ajax_outlets_by_channel, name='ajax_outlets_by_channel'),

    # ============================================================================
    # CATALOG CASCADE: Brand → Category → Product
    # ============================================================================
    path('ajax/categories/', ajax_views.ajax_categories_by_brand, name='ajax_categories_by_brand'),
    path('ajax/products/', ajax_views.ajax_products_search, name='ajax_products_search'),

    # ============================================================================
    # STATISTICS & AGGREGATION
    # ============================================================================
    path('ajax/outlet-stats/', ajax_views.ajax_outlet_stats, name='ajax_outlet_stats'),
    path('ajax/region-summary/', ajax_views.ajax_region_summary, name='ajax_region_summary'),

    # ============================================================================
    # ATTRIBUTE SYSTEM
    # ============================================================================
    path('ajax/attribute-info/<int:attribute_id>/', ajax_views.ajax_attribute_info, name='ajax_attribute_info'),
    path('ajax/attributes-by-category/', ajax_views.ajax_attributes_by_category, name='ajax_attributes_by_category'),
    path('ajax/attribute-groups/', ajax_views.ajax_attribute_groups_by_category, name='ajax_attribute_groups_by_category'),
    path('ajax/products-with-attribute/', ajax_views.ajax_products_with_attribute, name='ajax_products_with_attribute'),

    # ============================================================================
    # VISUAL CONSTRUCTORS
    # ============================================================================
    path('coefficients/', ajax_views.coefficients_api, name='coefficients_api'),
]
