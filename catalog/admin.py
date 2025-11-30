from django.contrib import admin
from .models import (
    Brand, Category, Product,
    AttributeGroup, AttributeDefinition,
    ProductAttributeValue, CategoryAttributeTemplate
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country', 'created_at', 'updated_at']
    list_filter = ['country', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'logo')
        }),
        ('Details', {
            'fields': ('description', 'country', 'settings')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'parent', 'created_at', 'updated_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'code', 'parent')
        }),
        ('Details', {
            'fields': ('description', 'settings')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku_code', 'brand', 'category', 'status', 'price', 'created_at']
    list_filter = ['status', 'brand', 'category', 'created_at']
    search_fields = ['name', 'sku_code', 'brand__name', 'category__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['brand', 'category', 'name']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'sku_code', 'brand', 'category', 'status')
        }),
        ('Details', {
            'fields': ('description', 'image', 'weight', 'price')
        }),
        ('Attributes', {
            'fields': ('attributes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============================================================================
# EAV SYSTEM ADMIN
# ============================================================================

@admin.register(AttributeGroup)
class AttributeGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'category__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['category', 'order', 'name']
    list_per_page = 25
    list_editable = ['order', 'is_active']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'code', 'category')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AttributeDefinition)
class AttributeDefinitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'group', 'data_type', 'is_required', 'is_filterable', 'is_active', 'order']
    list_filter = ['data_type', 'is_required', 'is_filterable', 'is_searchable', 'is_active', 'group']
    search_fields = ['name', 'code', 'group__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['group', 'order', 'name']
    list_per_page = 25
    list_editable = ['order', 'is_active']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'code', 'group', 'data_type')
        }),
        ('Настройки валидации', {
            'fields': ('is_required', 'is_filterable', 'is_searchable')
        }),
        ('Параметры для числовых типов', {
            'fields': ('min_value', 'max_value'),
            'classes': ('collapse',)
        }),
        ('Параметры для текстовых типов', {
            'fields': ('max_length',),
            'classes': ('collapse',)
        }),
        ('Параметры для выбора', {
            'fields': ('choices',),
            'classes': ('collapse',),
            'description': 'Введите JSON список: ["Вариант 1", "Вариант 2"]'
        }),
        ('UI настройки', {
            'fields': ('unit', 'placeholder', 'help_text'),
            'classes': ('collapse',)
        }),
        ('Порядок и активность', {
            'fields': ('order', 'is_active')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1
    fields = ['attribute', 'value_text', 'value_integer', 'value_decimal', 'value_boolean', 'value_date', 'value_choice']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['product', 'attribute', 'get_value', 'created_at']
    list_filter = ['attribute', 'product__category', 'created_at']
    search_fields = ['product__name', 'attribute__name']
    readonly_fields = ['created_at', 'updated_at', 'get_value']
    ordering = ['product', 'attribute__group', 'attribute__order']
    list_per_page = 25

    fieldsets = (
        ('Основная информация', {
            'fields': ('product', 'attribute')
        }),
        ('Значения', {
            'fields': (
                'value_text', 'value_integer', 'value_decimal',
                'value_boolean', 'value_date', 'value_choice',
                'value_multi_choice', 'value_file'
            )
        }),
        ('Текущее значение', {
            'fields': ('get_value',),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CategoryAttributeTemplate)
class CategoryAttributeTemplateAdmin(admin.ModelAdmin):
    list_display = ['category', 'attribute', 'is_required', 'order']
    list_filter = ['category', 'is_required', 'attribute__data_type']
    search_fields = ['category__name', 'attribute__name']
    ordering = ['category', 'order']
    list_per_page = 25
    list_editable = ['is_required', 'order']

    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'attribute')
        }),
        ('Настройки', {
            'fields': ('is_required', 'order')
        }),
    )
