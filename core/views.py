from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import datetime, timedelta

from geo.models import GlobalMarket, Country, Region, Channel, Outlet
from catalog.models import Brand, Category, Product, AttributeDefinition, ProductAttributeValue
from visits.models import Visit
from forms.models import FormTemplate


@login_required
def home(request):
    """Главная страница с дашбордом"""

    # Основная статистика
    stats = {
        'global_markets': GlobalMarket.objects.count(),
        'countries': Country.objects.count(),
        'regions': Region.objects.count(),
        'channels': Channel.objects.count(),
        'outlets': Outlet.objects.count(),
        'brands': Brand.objects.count(),
        'categories': Category.objects.count(),
        'products': Product.objects.count(),
        'visits': Visit.objects.count(),
        'forms': FormTemplate.objects.count(),
    }

    # EAV статистика
    eav_stats = {
        'attributes': AttributeDefinition.objects.filter(is_active=True).count(),
        'attribute_groups': AttributeDefinition.objects.values('group').distinct().count(),
        'products_with_attributes': Product.objects.filter(attribute_values__isnull=False).distinct().count(),
        'total_attribute_values': ProductAttributeValue.objects.count(),
    }

    # Последние визиты
    recent_visits = Visit.objects.select_related(
        'outlet', 'visit_type', 'user'
    ).order_by('-created_at')[:5]

    # Последние добавленные товары
    recent_products = Product.objects.select_related(
        'brand', 'category'
    ).order_by('-created_at')[:5]

    # Статистика по статусам товаров
    product_status_stats = Product.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')

    # Топ категорий по количеству товаров
    top_categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0).order_by('-product_count')[:5]

    # Топ брендов по количеству товаров
    top_brands = Brand.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0).order_by('-product_count')[:5]

    # Визиты за последние 6 месяцев
    today = datetime.now()
    visits_by_month = []
    month_labels = []

    for i in range(5, -1, -1):
        month_date = today - timedelta(days=30*i)
        month_start = month_date.replace(day=1)
        if i == 0:
            month_end = today
        else:
            next_month = month_start.replace(day=28) + timedelta(days=4)
            month_end = next_month.replace(day=1) - timedelta(days=1)

        count = Visit.objects.filter(
            created_at__gte=month_start,
            created_at__lte=month_end
        ).count()

        visits_by_month.append(count)
        month_labels.append(month_date.strftime('%b'))

    context = {
        'stats': stats,
        'eav_stats': eav_stats,
        'recent_visits': recent_visits,
        'recent_products': recent_products,
        'product_status_stats': product_status_stats,
        'top_categories': top_categories,
        'top_brands': top_brands,
        'visits_by_month': visits_by_month,
        'month_labels': month_labels,
    }
    return render(request, 'home.html', context)
