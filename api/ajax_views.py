"""
AJAX Views for dynamic data loading and cascading dropdowns
Compatible with Select2 library format
"""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from geo.models import GlobalMarket, Country, Region, City, District, Channel, Outlet
from catalog.models import Brand, Category, Product, AttributeDefinition, AttributeGroup
from coefficients.models import Coefficient


# ============================================================================
# GEO CASCADE: GlobalMarket → Country → Region → City → District → Channel → Outlet
# ============================================================================

@login_required
def ajax_countries_by_globalmarket(request):
    """
    Load countries filtered by global market
    GET params: globalmarket (id), q (search term)
    """
    globalmarket_id = request.GET.get('globalmarket', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    countries = Country.objects.select_related('global_market').only('id', 'name', 'code', 'global_market__name')

    # Filter by global market
    if globalmarket_id:
        countries = countries.filter(global_market_id=globalmarket_id)

    # Search filter
    if search_term:
        countries = countries.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term)
        )

    # Pagination
    total_count = countries.count()
    start = (page - 1) * page_size
    end = start + page_size
    countries = countries[start:end]

    # Format for Select2
    results = [
        {
            'id': country.id,
            'text': f"{country.name} ({country.code})",
            'name': country.name,
            'code': country.code,
            'globalmarket': country.global_market.name if country.global_market else '-'
        }
        for country in countries
    ]

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total_count}
    })


@login_required
def ajax_regions_by_country(request):
    """
    Load regions filtered by country
    GET params: country (id), q (search term)
    """
    country_id = request.GET.get('country', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    regions = Region.objects.select_related('country').only('id', 'name', 'code', 'country__name')

    # Filter by country
    if country_id:
        regions = regions.filter(country_id=country_id)

    # Search filter
    if search_term:
        regions = regions.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term)
        )

    # Pagination
    total_count = regions.count()
    start = (page - 1) * page_size
    end = start + page_size
    regions = regions[start:end]

    # Format for Select2
    results = [
        {
            'id': region.id,
            'text': f"{region.name} ({region.code})",
            'name': region.name,
            'code': region.code,
            'country': region.country.name if region.country else '-'
        }
        for region in regions
    ]

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total_count}
    })


@login_required
def ajax_cities_by_region(request):
    """
    Load cities filtered by region
    GET params: region (id), q (search term)
    """
    region_id = request.GET.get('region', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    cities = City.objects.select_related('region').only('id', 'name', 'code', 'region__name')

    # Filter by region
    if region_id:
        cities = cities.filter(region_id=region_id)

    # Search filter
    if search_term:
        cities = cities.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term)
        )

    # Pagination
    total_count = cities.count()
    start = (page - 1) * page_size
    end = start + page_size
    cities = cities[start:end]

    # Format for Select2
    results = [
        {
            'id': city.id,
            'text': f"{city.name} ({city.code})",
            'name': city.name,
            'code': city.code,
            'region': city.region.name if city.region else '-'
        }
        for city in cities
    ]

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total_count}
    })


@login_required
def ajax_districts_by_city(request):
    """
    Load districts filtered by city
    GET params: city (id), q (search term)
    """
    city_id = request.GET.get('city', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    districts = District.objects.select_related('city').only('id', 'name', 'code', 'city__name')

    # Filter by city
    if city_id:
        districts = districts.filter(city_id=city_id)

    # Search filter
    if search_term:
        districts = districts.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term)
        )

    # Pagination
    total_count = districts.count()
    start = (page - 1) * page_size
    end = start + page_size
    districts = districts[start:end]

    # Format for Select2
    results = [
        {
            'id': district.id,
            'text': f"{district.name} ({district.code})",
            'name': district.name,
            'code': district.code,
            'city': district.city.name if district.city else '-'
        }
        for district in districts
    ]

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total_count}
    })


@login_required
def ajax_channels_by_district(request):
    """
    Load channels filtered by district
    GET params: district (id), q (search term)
    """
    district_id = request.GET.get('district', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    channels = Channel.objects.select_related('district').only('id', 'name', 'code', 'district__name')

    # Filter by district
    if district_id:
        channels = channels.filter(district_id=district_id)

    # Search filter
    if search_term:
        channels = channels.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term)
        )

    # Pagination
    total_count = channels.count()
    start = (page - 1) * page_size
    end = start + page_size
    channels = channels[start:end]

    # Format for Select2
    results = [
        {
            'id': channel.id,
            'text': f"{channel.name} ({channel.code})",
            'name': channel.name,
            'code': channel.code,
            'district': channel.district.name if channel.district else '-'
        }
        for channel in channels
    ]

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total_count}
    })


@login_required
def ajax_outlets_by_channel(request):
    """
    Load outlets filtered by channel
    GET params: channel (id), district (id), city (id), region (id), q (search term)
    """
    channel_id = request.GET.get('channel', '').strip()
    district_id = request.GET.get('district', '').strip()
    city_id = request.GET.get('city', '').strip()
    region_id = request.GET.get('region', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    outlets = Outlet.objects.select_related('channel', 'channel__district', 'channel__district__city', 'channel__district__city__region').only(
        'id', 'name', 'code', 'address', 'channel__name', 'channel__district__name', 'channel__district__city__name', 'channel__district__city__region__name'
    )

    # Filter by channel
    if channel_id:
        outlets = outlets.filter(channel_id=channel_id)

    # Alternative filter by district (shows all outlets in district)
    elif district_id:
        outlets = outlets.filter(channel__district_id=district_id)

    # Alternative filter by city (shows all outlets in city)
    elif city_id:
        outlets = outlets.filter(channel__district__city_id=city_id)

    # Alternative filter by region (shows all outlets in region)
    elif region_id:
        outlets = outlets.filter(channel__district__city__region_id=region_id)

    # Search filter
    if search_term:
        outlets = outlets.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term) |
            Q(address__icontains=search_term)
        )

    # Pagination
    total_count = outlets.count()
    start = (page - 1) * page_size
    end = start + page_size
    outlets = outlets[start:end]

    # Format for Select2
    results = [
        {
            'id': outlet.id,
            'text': f"{outlet.name} - {outlet.address[:50] if outlet.address else 'Нет адреса'}",
            'name': outlet.name,
            'code': outlet.code,
            'address': outlet.address,
            'channel': outlet.channel.name if outlet.channel else '-',
            'district': outlet.channel.district.name if outlet.channel and outlet.channel.district else '-',
            'city': outlet.channel.district.city.name if outlet.channel and outlet.channel.district and outlet.channel.district.city else '-',
            'region': outlet.channel.district.city.region.name if outlet.channel and outlet.channel.district and outlet.channel.district.city and outlet.channel.district.city.region else '-'
        }
        for outlet in outlets
    ]

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total_count}
    })


# ============================================================================
# CATALOG CASCADE: Brand → Category → Product
# ============================================================================

@login_required
def ajax_categories_by_brand(request):
    """
    Load categories filtered by brand
    GET params: brand (id), q (search term)
    """
    brand_id = request.GET.get('brand', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    # Get categories that have products of this brand
    categories = Category.objects.only('id', 'name', 'code')

    if brand_id:
        # Filter categories that contain products from this brand
        categories = categories.filter(products__brand_id=brand_id).distinct()

    # Search filter
    if search_term:
        categories = categories.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term)
        )

    # Pagination
    total_count = categories.count()
    start = (page - 1) * page_size
    end = start + page_size
    categories = categories[start:end]

    # Format for Select2
    results = [
        {
            'id': category.id,
            'text': f"{category.name} ({category.code})",
            'name': category.name,
            'code': category.code
        }
        for category in categories
    ]

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total_count}
    })


@login_required
def ajax_products_search(request):
    """
    Search products with multiple filters
    GET params: brand (id), category (id), q (search term)
    """
    brand_id = request.GET.get('brand', '').strip()
    category_id = request.GET.get('category', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    products = Product.objects.select_related('brand', 'category').only(
        'id', 'name', 'code', 'sku', 'brand__name', 'category__name'
    )

    # Filter by brand
    if brand_id:
        products = products.filter(brand_id=brand_id)

    # Filter by category
    if category_id:
        products = products.filter(category_id=category_id)

    # Search filter
    if search_term:
        products = products.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term) |
            Q(sku__icontains=search_term) |
            Q(barcode__icontains=search_term)
        )

    # Pagination
    total_count = products.count()
    start = (page - 1) * page_size
    end = start + page_size
    products = products[start:end]

    # Format for Select2
    results = [
        {
            'id': product.id,
            'text': f"{product.name} ({product.sku})",
            'name': product.name,
            'code': product.code,
            'sku': product.sku,
            'brand': product.brand.name if product.brand else '-',
            'category': product.category.name if product.category else '-'
        }
        for product in products
    ]

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total_count}
    })


# ============================================================================
# STATISTICS & AGGREGATION ENDPOINTS
# ============================================================================

@login_required
def ajax_outlet_stats(request):
    """
    Get statistics for a specific outlet
    GET params: outlet_id
    """
    outlet_id = request.GET.get('outlet_id', '').strip()

    if not outlet_id:
        return JsonResponse({'error': 'outlet_id required'}, status=400)

    try:
        from visits.models import Visit, Observation

        outlet = Outlet.objects.get(pk=outlet_id)

        # Count visits
        visits_count = Visit.objects.filter(outlet_id=outlet_id).count()

        # Count observations
        observations_count = Observation.objects.filter(visit__outlet_id=outlet_id).count()

        # Get unique products observed
        unique_products = Observation.objects.filter(
            visit__outlet_id=outlet_id
        ).values('product').distinct().count()

        return JsonResponse({
            'outlet': {
                'id': outlet.id,
                'name': outlet.name,
                'code': outlet.code,
                'address': outlet.address
            },
            'stats': {
                'visits_count': visits_count,
                'observations_count': observations_count,
                'unique_products': unique_products
            }
        })
    except Outlet.DoesNotExist:
        return JsonResponse({'error': 'Outlet not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def ajax_region_summary(request):
    """
    Get summary statistics for a region
    GET params: region_id
    """
    region_id = request.GET.get('region_id', '').strip()

    if not region_id:
        return JsonResponse({'error': 'region_id required'}, status=400)

    try:
        region = Region.objects.get(pk=region_id)

        # Count channels (through district -> city -> region)
        channels_count = Channel.objects.filter(district__city__region_id=region_id).count()

        # Count outlets (through channel -> district -> city -> region)
        outlets_count = Outlet.objects.filter(channel__district__city__region_id=region_id).count()

        # Count visits
        from visits.models import Visit
        visits_count = Visit.objects.filter(outlet__channel__district__city__region_id=region_id).count()

        return JsonResponse({
            'region': {
                'id': region.id,
                'name': region.name,
                'code': region.code
            },
            'stats': {
                'channels_count': channels_count,
                'outlets_count': outlets_count,
                'visits_count': visits_count
            }
        })
    except Region.DoesNotExist:
        return JsonResponse({'error': 'Region not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# ATTRIBUTE SYSTEM AJAX ENDPOINTS
# ============================================================================

@login_required
def ajax_attribute_info(request, attribute_id):
    """
    Get attribute definition information (data type, constraints, etc.)
    Used for dynamic form field display
    """
    try:
        attribute = AttributeDefinition.objects.get(id=attribute_id)
        return JsonResponse({
            'id': attribute.id,
            'name': attribute.name,
            'code': attribute.code,
            'data_type': attribute.data_type,
            'is_required': attribute.is_required,
            'is_filterable': attribute.is_filterable,
            'min_value': float(attribute.min_value) if attribute.min_value else None,
            'max_value': float(attribute.max_value) if attribute.max_value else None,
            'max_length': attribute.max_length,
            'choices': attribute.choices,
            'unit': attribute.unit,
            'placeholder': attribute.placeholder,
            'help_text': attribute.help_text
        })
    except AttributeDefinition.DoesNotExist:
        return JsonResponse({'error': 'Attribute not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def ajax_attributes_by_category(request):
    """
    Load attributes filtered by category
    GET params: category (id), q (search term)
    Returns attributes that belong to groups of the specified category
    """
    category_id = request.GET.get('category', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    attributes = AttributeDefinition.objects.select_related('group').filter(is_active=True)

    # Filter by category through group
    if category_id:
        attributes = attributes.filter(group__category_id=category_id)

    # Search filter
    if search_term:
        attributes = attributes.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term)
        )

    # Pagination
    total_count = attributes.count()
    start = (page - 1) * page_size
    end = start + page_size
    attributes = attributes[start:end]

    # Format for Select2
    results = [
        {
            'id': attr.id,
            'text': f"{attr.name}" + (f" ({attr.unit})" if attr.unit else ""),
            'data_type': attr.data_type,
            'group': attr.group.name if attr.group else None
        }
        for attr in attributes
    ]

    return JsonResponse({
        'results': results,
        'pagination': {
            'more': end < total_count
        }
    })


@login_required
def ajax_attribute_groups_by_category(request):
    """
    Load attribute groups filtered by category
    GET params: category (id), q (search term)
    """
    category_id = request.GET.get('category', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    groups = AttributeGroup.objects.filter(is_active=True)

    # Filter by category
    if category_id:
        groups = groups.filter(category_id=category_id)

    # Search filter
    if search_term:
        groups = groups.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term)
        )

    # Pagination
    total_count = groups.count()
    start = (page - 1) * page_size
    end = start + page_size
    groups = groups[start:end]

    # Format for Select2
    results = [
        {
            'id': group.id,
            'text': group.name
        }
        for group in groups
    ]

    return JsonResponse({
        'results': results,
        'pagination': {
            'more': end < total_count
        }
    })


@login_required
def ajax_products_with_attribute(request):
    """
    Search products by attribute value
    GET params: attribute_id, value, q (search term)
    Used for filtering products by their attributes
    """
    attribute_id = request.GET.get('attribute_id', '').strip()
    value = request.GET.get('value', '').strip()
    search_term = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    if not attribute_id:
        return JsonResponse({'error': 'attribute_id is required'}, status=400)

    try:
        attribute = AttributeDefinition.objects.get(id=attribute_id)
    except AttributeDefinition.DoesNotExist:
        return JsonResponse({'error': 'Attribute not found'}, status=404)

    # Build query based on attribute data type
    from catalog.models import ProductAttributeValue
    query = ProductAttributeValue.objects.filter(attribute_id=attribute_id)

    # Filter by value based on data type
    if value:
        if attribute.data_type == 'text':
            query = query.filter(value_text__icontains=value)
        elif attribute.data_type == 'integer':
            query = query.filter(value_integer=int(value))
        elif attribute.data_type == 'decimal':
            query = query.filter(value_decimal=float(value))
        elif attribute.data_type == 'boolean':
            query = query.filter(value_boolean=(value.lower() == 'true'))
        elif attribute.data_type == 'choice':
            query = query.filter(value_choice=value)

    # Get products
    product_ids = query.values_list('product_id', flat=True)
    products = Product.objects.filter(id__in=product_ids).select_related('brand', 'category')

    # Additional search filter
    if search_term:
        products = products.filter(
            Q(name__icontains=search_term) |
            Q(sku_code__icontains=search_term)
        )

    # Pagination
    total_count = products.count()
    start = (page - 1) * page_size
    end = start + page_size
    products = products[start:end]

    # Format results
    results = [
        {
            'id': product.id,
            'text': f"{product.name} - {product.brand.name}",
            'sku': product.sku_code,
            'category': product.category.name
        }
        for product in products
    ]

    return JsonResponse({
        'results': results,
        'pagination': {
            'more': end < total_count
        },
        'total_count': total_count
    })


# ============================================================================
# VISUAL CONSTRUCTORS
# ============================================================================

@login_required
def coefficients_api(request):
    """
    API для получения списка коэффициентов (для визуального конструктора дашбордов)
    GET params:
        q (search term) - optional
        data_type (MON/EXP/AI) - фильтр по типу источника данных
    """
    search_term = request.GET.get('q', '').strip()
    data_type = request.GET.get('data_type', '').strip()

    coefficients = Coefficient.objects.filter(is_active=True).only(
        'id', 'name', 'code', 'unit', 'value_type', 'data_type'
    )

    # Filter by data_type (MON/EXP/AI)
    if data_type in ['MON', 'EXP', 'AI']:
        coefficients = coefficients.filter(data_type=data_type)

    # Search filter
    if search_term:
        coefficients = coefficients.filter(
            Q(name__icontains=search_term) |
            Q(code__icontains=search_term)
        )

    # Convert to list
    results = [
        {
            'id': coef.id,
            'name': coef.name,
            'code': coef.code,
            'unit': coef.unit if coef.unit else '',
            'value_type': coef.value_type,
            'data_type': coef.data_type,
            'data_type_display': coef.get_data_type_display()
        }
        for coef in coefficients
    ]

    return JsonResponse(results, safe=False)
