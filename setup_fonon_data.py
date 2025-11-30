"""
Management script to setup FONON jewelry retail data collection system
Создает все необходимые коэффициенты, категории, атрибуты, метрики, формулы для сбора данных
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datum.settings')
django.setup()

from catalog.models import Category, AttributeGroup, AttributeDefinition
from coefficients.models import Coefficient, Metric, Formula
from forms.models import FormTemplate
import json


def setup_categories():
    """Создать категории ювелирных изделий"""
    print("🏷️  Создание категорий...")

    categories_data = [
        {'name': 'Кольца', 'code': 'rings'},
        {'name': 'Серьги', 'code': 'earrings'},
        {'name': 'Цепочки', 'code': 'chains'},
        {'name': 'Браслеты', 'code': 'bracelets'},
        {'name': 'Кулоны', 'code': 'pendants'},
        {'name': 'Комплекты', 'code': 'sets'},
    ]

    created = []
    for data in categories_data:
        cat, created_flag = Category.objects.get_or_create(
            code=data['code'],
            defaults={'name': data['name']}
        )
        if created_flag:
            created.append(cat.name)
            print(f"   ✅ {cat.name}")
        else:
            print(f"   ⏭️  {cat.name} (уже существует)")

    return Category.objects.filter(code__in=[c['code'] for c in categories_data])


def setup_attributes(categories):
    """Создать атрибуты для ювелирных изделий"""
    print("\n🏗️  Создание групп атрибутов...")

    # Группа "Металл"
    for category in categories:
        metal_group, created = AttributeGroup.objects.get_or_create(
            code=f'metal_{category.code}',
            category=category,
            defaults={
                'name': 'Металл',
                'order': 1
            }
        )
        if created:
            print(f"   ✅ Группа 'Металл' для {category.name}")

        # Атрибуты металла
        attrs = [
            {
                'name': 'Цвет металла',
                'code': f'metal_color_{category.code}',
                'data_type': 'choice',
                'choices': ['Желтое золото', 'Белое золото', 'Красное золото', 'Платина', 'Серебро']
            },
            {
                'name': 'Проба',
                'code': f'metal_grade_{category.code}',
                'data_type': 'choice',
                'choices': ['375', '500', '585', '750', '900', '925', '950']
            },
            {
                'name': 'Вес металла (гр)',
                'code': f'metal_weight_{category.code}',
                'data_type': 'decimal',
            }
        ]

        for attr_data in attrs:
            attr, created = AttributeDefinition.objects.get_or_create(
                code=attr_data['code'],
                defaults={
                    'name': attr_data['name'],
                    'group': metal_group,
                    'data_type': attr_data['data_type'],
                    'choices': json.dumps(attr_data.get('choices', [])) if 'choices' in attr_data else None
                }
            )
            if created:
                print(f"      ✅ {attr.name}")

        # Группа "Камни" (только для премиум)
        stones_group, created = AttributeGroup.objects.get_or_create(
            code=f'stones_{category.code}',
            category=category,
            defaults={
                'name': 'Камни',
                'order': 2
            }
        )
        if created:
            print(f"   ✅ Группа 'Камни' для {category.name}")

        stone_attrs = [
            {
                'name': 'Наличие камней',
                'code': f'has_stones_{category.code}',
                'data_type': 'boolean',
            },
            {
                'name': 'Тип камней',
                'code': f'stone_type_{category.code}',
                'data_type': 'choice',
                'choices': ['Бриллианты', 'Изумруды', 'Рубины', 'Сапфиры', 'Фианиты', 'Другие']
            },
        ]

        for attr_data in stone_attrs:
            attr, created = AttributeDefinition.objects.get_or_create(
                code=attr_data['code'],
                defaults={
                    'name': attr_data['name'],
                    'group': stones_group,
                    'data_type': attr_data['data_type'],
                    'choices': json.dumps(attr_data.get('choices', [])) if 'choices' in attr_data else None
                }
            )
            if created:
                print(f"      ✅ {attr.name}")


def setup_coefficients():
    """Создать все коэффициенты для сбора данных FONON"""
    print("\n📊 Создание коэффициентов...")

    coefficients_data = [
        # 1. Проходимость
        {
            'name': 'Проходимость',
            'code': 'passability',
            'description': 'Количество посетителей в час',
            'unit': 'чел./час',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },

        # 2. Количество прилавков
        {
            'name': 'Количество прилавков',
            'code': 'counter_count',
            'description': 'Количество прилавков в магазине',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },

        # 3. Всего изделий в магазине
        {
            'name': 'Всего изделий в магазине',
            'code': 'total_products_store',
            'description': 'Общее количество изделий в магазине',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },

        # 4. Всего изделий на прилавке
        {
            'name': 'Изделий на прилавке',
            'code': 'products_per_counter',
            'description': 'Количество изделий на одном прилавке',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },

        # 5. Премиум сегмент
        {
            'name': 'Количество премиум изделий',
            'code': 'premium_count',
            'description': 'Изделия с драгоценными камнями',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },

        # 6-8. По типу металла
        {
            'name': 'Изделия из желтого золота',
            'code': 'yellow_gold_count',
            'description': 'Количество изделий из желтого золота',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Изделия из красного золота',
            'code': 'red_gold_count',
            'description': 'Количество изделий из красного золота',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Изделия из белого золота',
            'code': 'white_gold_count',
            'description': 'Количество изделий из белого золота',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },

        # 9-13. По категориям
        {
            'name': 'Количество колец',
            'code': 'rings_count',
            'description': 'Количество колец в наличии',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Количество серег',
            'code': 'earrings_count',
            'description': 'Количество серег в наличии',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Количество цепочек',
            'code': 'chains_count',
            'description': 'Количество цепочек в наличии',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Количество браслетов',
            'code': 'bracelets_count',
            'description': 'Количество браслетов в наличии',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Количество кулонов',
            'code': 'pendants_count',
            'description': 'Количество кулонов в наличии',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },

        # 14-18. Суммарный вес по категориям (для расчета среднего)
        {
            'name': 'Суммарный вес колец',
            'code': 'rings_total_weight',
            'description': 'Общий вес всех колец',
            'unit': 'гр',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Суммарный вес серег',
            'code': 'earrings_total_weight',
            'description': 'Общий вес всех серег',
            'unit': 'гр',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Суммарный вес цепочек',
            'code': 'chains_total_weight',
            'description': 'Общий вес всех цепочек',
            'unit': 'гр',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Суммарный вес браслетов',
            'code': 'bracelets_total_weight',
            'description': 'Общий вес всех браслетов',
            'unit': 'гр',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Суммарный вес кулонов',
            'code': 'pendants_total_weight',
            'description': 'Общий вес всех кулонов',
            'unit': 'гр',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },

        # 19-20. Комплекты
        {
            'name': 'Количество комплектов',
            'code': 'sets_count',
            'description': 'Количество комплектов в наличии',
            'unit': 'шт',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },
        {
            'name': 'Суммарный вес комплектов',
            'code': 'sets_total_weight',
            'description': 'Общий вес всех комплектов',
            'unit': 'гр',
            'value_type': 'numeric',
            'data_type': 'MON',
            'applies_to_outlet': True,
        },

        # 21. Продажи
        {
            'name': 'Продаж в час',
            'code': 'sales_per_hour',
            'description': 'Количество продаж в час',
            'unit': 'шт/час',
            'value_type': 'numeric',
            'data_type': 'EXP',
            'applies_to_outlet': True,
        },
        {
            'name': 'Продаж в день',
            'code': 'sales_per_day',
            'description': 'Количество продаж за день',
            'unit': 'шт/день',
            'value_type': 'numeric',
            'data_type': 'EXP',
            'applies_to_outlet': True,
        },

        # Дополнительные коэффициенты для детализации продаж
        {
            'name': 'Продажи колец в день',
            'code': 'rings_sales_per_day',
            'description': 'Продажи колец за день',
            'unit': 'шт/день',
            'value_type': 'numeric',
            'data_type': 'EXP',
            'applies_to_outlet': True,
        },
        {
            'name': 'Продажи серег в день',
            'code': 'earrings_sales_per_day',
            'description': 'Продажи серег за день',
            'unit': 'шт/день',
            'value_type': 'numeric',
            'data_type': 'EXP',
            'applies_to_outlet': True,
        },
        {
            'name': 'Продажи цепочек в день',
            'code': 'chains_sales_per_day',
            'description': 'Продажи цепочек за день',
            'unit': 'шт/день',
            'value_type': 'numeric',
            'data_type': 'EXP',
            'applies_to_outlet': True,
        },
        {
            'name': 'Продажи браслетов в день',
            'code': 'bracelets_sales_per_day',
            'description': 'Продажи браслетов за день',
            'unit': 'шт/день',
            'value_type': 'numeric',
            'data_type': 'EXP',
            'applies_to_outlet': True,
        },
        {
            'name': 'Продажи кулонов в день',
            'code': 'pendants_sales_per_day',
            'description': 'Продажи кулонов за день',
            'unit': 'шт/день',
            'value_type': 'numeric',
            'data_type': 'EXP',
            'applies_to_outlet': True,
        },
    ]

    created_coefficients = {}
    for data in coefficients_data:
        coef, created = Coefficient.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        created_coefficients[data['code']] = coef
        if created:
            print(f"   ✅ {coef.name}")
        else:
            print(f"   ⏭️  {coef.name} (уже существует)")

    return created_coefficients


def setup_formulas(coefficients):
    """Создать формулы для расчетных метрик"""
    print("\n🧮 Создание формул...")

    formulas_data = [
        # Доля премиум сегмента
        {
            'name': 'Доля премиум сегмента',
            'code': 'premium_share',
            'description': 'Процент изделий с драгоценными камнями',
            'expression': '(C1 / C2) * 100',
            'coefficient_map': {
                'C1': 'premium_count',
                'C2': 'total_products_store'
            }
        },
        # Доля по типу металла
        {
            'name': 'Доля желтого золота',
            'code': 'yellow_gold_share',
            'description': 'Процент изделий из желтого золота',
            'expression': '(C1 / C2) * 100',
            'coefficient_map': {
                'C1': 'yellow_gold_count',
                'C2': 'total_products_store'
            }
        },
        {
            'name': 'Доля красного золота',
            'code': 'red_gold_share',
            'description': 'Процент изделий из красного золота',
            'expression': '(C1 / C2) * 100',
            'coefficient_map': {
                'C1': 'red_gold_count',
                'C2': 'total_products_store'
            }
        },
        {
            'name': 'Доля белого золота',
            'code': 'white_gold_share',
            'description': 'Процент изделий из белого золота',
            'expression': '(C1 / C2) * 100',
            'coefficient_map': {
                'C1': 'white_gold_count',
                'C2': 'total_products_store'
            }
        },
        # Средний вес по категориям
        {
            'name': 'Средний вес кольца',
            'code': 'avg_ring_weight',
            'description': 'Средний вес одного кольца',
            'expression': 'C1 / C2',
            'coefficient_map': {
                'C1': 'rings_total_weight',
                'C2': 'rings_count'
            }
        },
        {
            'name': 'Средний вес серег',
            'code': 'avg_earring_weight',
            'description': 'Средний вес одной пары серег',
            'expression': 'C1 / C2',
            'coefficient_map': {
                'C1': 'earrings_total_weight',
                'C2': 'earrings_count'
            }
        },
        {
            'name': 'Средний вес цепочки',
            'code': 'avg_chain_weight',
            'description': 'Средний вес одной цепочки',
            'expression': 'C1 / C2',
            'coefficient_map': {
                'C1': 'chains_total_weight',
                'C2': 'chains_count'
            }
        },
        {
            'name': 'Средний вес браслета',
            'code': 'avg_bracelet_weight',
            'description': 'Средний вес одного браслета',
            'expression': 'C1 / C2',
            'coefficient_map': {
                'C1': 'bracelets_total_weight',
                'C2': 'bracelets_count'
            }
        },
        {
            'name': 'Средний вес кулона',
            'code': 'avg_pendant_weight',
            'description': 'Средний вес одного кулона',
            'expression': 'C1 / C2',
            'coefficient_map': {
                'C1': 'pendants_total_weight',
                'C2': 'pendants_count'
            }
        },
        {
            'name': 'Средний вес комплекта',
            'code': 'avg_set_weight',
            'description': 'Средний вес одного комплекта',
            'expression': 'C1 / C2',
            'coefficient_map': {
                'C1': 'sets_total_weight',
                'C2': 'sets_count'
            }
        },
    ]

    created_formulas = {}
    for data in formulas_data:
        # Получить коэффициенты для формулы
        coef_ids = {}
        for placeholder, code in data['coefficient_map'].items():
            if code in coefficients:
                coef_ids[placeholder] = coefficients[code].id

        formula, created = Formula.objects.get_or_create(
            code=data['code'],
            defaults={
                'name': data['name'],
                'description': data['description'],
                'expression': data['expression'],
                'coefficient_map': coef_ids
            }
        )
        created_formulas[data['code']] = formula
        if created:
            print(f"   ✅ {formula.name}")
        else:
            print(f"   ⏭️  {formula.name} (уже существует)")

    return created_formulas


def setup_metrics(coefficients, formulas):
    """Создать метрики"""
    print("\n📈 Создание метрик...")

    metrics_data = [
        # Метрики на основе формул
        {
            'name': 'Доля премиум сегмента',
            'code': 'premium_share_metric',
            'description': 'Процент изделий с камнями от общего количества',
            'category': 'share',
            'formula': 'premium_share',
            'unit': '%',
            'target_value': 25.0,
        },
        {
            'name': 'Доля желтого золота',
            'code': 'yellow_gold_share_metric',
            'description': 'Процент изделий из желтого золота',
            'category': 'share',
            'formula': 'yellow_gold_share',
            'unit': '%',
        },
        {
            'name': 'Доля красного золота',
            'code': 'red_gold_share_metric',
            'description': 'Процент изделий из красного золота',
            'category': 'share',
            'formula': 'red_gold_share',
            'unit': '%',
        },
        {
            'name': 'Доля белого золота',
            'code': 'white_gold_share_metric',
            'description': 'Процент изделий из белого золота',
            'category': 'share',
            'formula': 'white_gold_share',
            'unit': '%',
        },
        # Средние веса
        {
            'name': 'Средний вес кольца',
            'code': 'avg_ring_weight_metric',
            'description': 'Средний вес кольца в граммах',
            'category': 'other',
            'formula': 'avg_ring_weight',
            'unit': 'гр',
        },
        {
            'name': 'Средний вес серег',
            'code': 'avg_earring_weight_metric',
            'description': 'Средний вес пары серег в граммах',
            'category': 'other',
            'formula': 'avg_earring_weight',
            'unit': 'гр',
        },
        {
            'name': 'Средний вес цепочки',
            'code': 'avg_chain_weight_metric',
            'description': 'Средний вес цепочки в граммах',
            'category': 'other',
            'formula': 'avg_chain_weight',
            'unit': 'гр',
        },
        {
            'name': 'Средний вес браслета',
            'code': 'avg_bracelet_weight_metric',
            'description': 'Средний вес браслета в граммах',
            'category': 'other',
            'formula': 'avg_bracelet_weight',
            'unit': 'гр',
        },
        {
            'name': 'Средний вес кулона',
            'code': 'avg_pendant_weight_metric',
            'description': 'Средний вес кулона в граммах',
            'category': 'other',
            'formula': 'avg_pendant_weight',
            'unit': 'гр',
        },
        {
            'name': 'Средний вес комплекта',
            'code': 'avg_set_weight_metric',
            'description': 'Средний вес комплекта в граммах',
            'category': 'other',
            'formula': 'avg_set_weight',
            'unit': 'гр',
        },
        # Простые метрики (без формул)
        {
            'name': 'Проходимость магазина',
            'code': 'passability_metric',
            'description': 'Среднее количество посетителей в час',
            'category': 'other',
            'unit': 'чел./час',
        },
        {
            'name': 'Продажи в день',
            'code': 'sales_per_day_metric',
            'description': 'Среднее количество продаж за день',
            'category': 'other',
            'unit': 'шт/день',
        },
    ]

    for data in metrics_data:
        formula_obj = formulas.get(data.get('formula')) if data.get('formula') else None

        metric, created = Metric.objects.get_or_create(
            code=data['code'],
            defaults={
                'name': data['name'],
                'description': data['description'],
                'category': data['category'],
                'formula': formula_obj,
                'unit': data.get('unit', ''),
                'target_value': data.get('target_value'),
            }
        )
        if created:
            print(f"   ✅ {metric.name}")
        else:
            print(f"   ⏭️  {metric.name} (уже существует)")


def setup_form_templates(coefficients):
    """Создать шаблоны форм для визитов"""
    print("\n📝 Создание шаблонов форм...")

    # Форма для мониторинга ювелирного магазина
    form_schema = [
        # Блок 1: Общая информация
        {
            'field_name': 'visit_date',
            'field_type': 'date',
            'label': 'Дата визита',
            'required': True,
            'order': 1,
            'section': 'general'
        },
        {
            'field_name': 'visit_time',
            'field_type': 'text',
            'label': 'Время визита',
            'required': True,
            'order': 2,
            'placeholder': 'Например: 14:30',
            'section': 'general'
        },
        {
            'field_name': 'passability',
            'field_type': 'number',
            'label': 'Проходимость (чел./час)',
            'required': True,
            'order': 3,
            'validation': {'min': 0},
            'section': 'general'
        },
        {
            'field_name': 'counter_count',
            'field_type': 'number',
            'label': 'Количество прилавков',
            'required': True,
            'order': 4,
            'validation': {'min': 1},
            'section': 'general'
        },

        # Блок 2: Подсчет изделий
        {
            'field_name': 'total_products_store',
            'field_type': 'number',
            'label': 'Всего изделий в магазине',
            'required': True,
            'order': 5,
            'validation': {'min': 0},
            'section': 'inventory'
        },
        {
            'field_name': 'products_per_counter',
            'field_type': 'number',
            'label': 'Изделий на одном прилавке (среднее)',
            'required': False,
            'order': 6,
            'validation': {'min': 0},
            'section': 'inventory'
        },
        {
            'field_name': 'premium_count',
            'field_type': 'number',
            'label': 'Изделия премиум (с камнями)',
            'required': True,
            'order': 7,
            'validation': {'min': 0},
            'section': 'inventory'
        },

        # Блок 3: По типу металла
        {
            'field_name': 'yellow_gold_count',
            'field_type': 'number',
            'label': 'Желтое золото (шт)',
            'required': True,
            'order': 8,
            'validation': {'min': 0},
            'section': 'metal'
        },
        {
            'field_name': 'red_gold_count',
            'field_type': 'number',
            'label': 'Красное золото (шт)',
            'required': True,
            'order': 9,
            'validation': {'min': 0},
            'section': 'metal'
        },
        {
            'field_name': 'white_gold_count',
            'field_type': 'number',
            'label': 'Белое золото (шт)',
            'required': True,
            'order': 10,
            'validation': {'min': 0},
            'section': 'metal'
        },

        # Блок 4: По категориям (количество)
        {
            'field_name': 'rings_count',
            'field_type': 'number',
            'label': 'Кольца (шт)',
            'required': True,
            'order': 11,
            'validation': {'min': 0},
            'section': 'categories'
        },
        {
            'field_name': 'earrings_count',
            'field_type': 'number',
            'label': 'Серьги (шт)',
            'required': True,
            'order': 12,
            'validation': {'min': 0},
            'section': 'categories'
        },
        {
            'field_name': 'chains_count',
            'field_type': 'number',
            'label': 'Цепочки (шт)',
            'required': True,
            'order': 13,
            'validation': {'min': 0},
            'section': 'categories'
        },
        {
            'field_name': 'bracelets_count',
            'field_type': 'number',
            'label': 'Браслеты (шт)',
            'required': True,
            'order': 14,
            'validation': {'min': 0},
            'section': 'categories'
        },
        {
            'field_name': 'pendants_count',
            'field_type': 'number',
            'label': 'Кулоны (шт)',
            'required': True,
            'order': 15,
            'validation': {'min': 0},
            'section': 'categories'
        },
        {
            'field_name': 'sets_count',
            'field_type': 'number',
            'label': 'Комплекты (шт)',
            'required': True,
            'order': 16,
            'validation': {'min': 0},
            'section': 'categories'
        },

        # Блок 5: Веса (опционально, для точных данных)
        {
            'field_name': 'rings_total_weight',
            'field_type': 'number',
            'label': 'Общий вес колец (гр)',
            'required': False,
            'order': 17,
            'validation': {'min': 0, 'step': 0.01},
            'section': 'weights'
        },
        {
            'field_name': 'earrings_total_weight',
            'field_type': 'number',
            'label': 'Общий вес серег (гр)',
            'required': False,
            'order': 18,
            'validation': {'min': 0, 'step': 0.01},
            'section': 'weights'
        },
        {
            'field_name': 'chains_total_weight',
            'field_type': 'number',
            'label': 'Общий вес цепочек (гр)',
            'required': False,
            'order': 19,
            'validation': {'min': 0, 'step': 0.01},
            'section': 'weights'
        },
        {
            'field_name': 'bracelets_total_weight',
            'field_type': 'number',
            'label': 'Общий вес браслетов (гр)',
            'required': False,
            'order': 20,
            'validation': {'min': 0, 'step': 0.01},
            'section': 'weights'
        },
        {
            'field_name': 'pendants_total_weight',
            'field_type': 'number',
            'label': 'Общий вес кулонов (гр)',
            'required': False,
            'order': 21,
            'validation': {'min': 0, 'step': 0.01},
            'section': 'weights'
        },
        {
            'field_name': 'sets_total_weight',
            'field_type': 'number',
            'label': 'Общий вес комплектов (гр)',
            'required': False,
            'order': 22,
            'validation': {'min': 0, 'step': 0.01},
            'section': 'weights'
        },

        # Блок 6: Продажи (экспертные данные)
        {
            'field_name': 'sales_per_hour',
            'field_type': 'number',
            'label': 'Продаж в час (со слов продавца)',
            'required': False,
            'order': 23,
            'validation': {'min': 0},
            'section': 'sales'
        },
        {
            'field_name': 'sales_per_day',
            'field_type': 'number',
            'label': 'Продаж за день (со слов продавца)',
            'required': False,
            'order': 24,
            'validation': {'min': 0},
            'section': 'sales'
        },
        {
            'field_name': 'rings_sales_per_day',
            'field_type': 'number',
            'label': 'Продажи колец/день',
            'required': False,
            'order': 25,
            'section': 'sales'
        },
        {
            'field_name': 'earrings_sales_per_day',
            'field_type': 'number',
            'label': 'Продажи серег/день',
            'required': False,
            'order': 26,
            'section': 'sales'
        },
        {
            'field_name': 'chains_sales_per_day',
            'field_type': 'number',
            'label': 'Продажи цепочек/день',
            'required': False,
            'order': 27,
            'section': 'sales'
        },
        {
            'field_name': 'bracelets_sales_per_day',
            'field_type': 'number',
            'label': 'Продажи браслетов/день',
            'required': False,
            'order': 28,
            'section': 'sales'
        },
        {
            'field_name': 'pendants_sales_per_day',
            'field_type': 'number',
            'label': 'Продажи кулонов/день',
            'required': False,
            'order': 29,
            'section': 'sales'
        },

        # Блок 7: Примечания
        {
            'field_name': 'notes',
            'field_type': 'textarea',
            'label': 'Примечания',
            'required': False,
            'order': 30,
            'placeholder': 'Дополнительные наблюдения...',
            'section': 'notes'
        },
    ]

    form_template, created = FormTemplate.objects.get_or_create(
        code='fonon_jewelry_monitoring',
        defaults={
            'name': 'FONON - Мониторинг ювелирного магазина',
            'description': 'Полная форма для сбора данных в ювелирной рознице',
            'form_type': 'visit',
            'fields_schema': form_schema,
            'category': 'jewelry',
            'status': 'active',
        }
    )

    if created:
        print(f"   ✅ Форма 'FONON - Мониторинг ювелирного магазина' создана")
    else:
        print(f"   ⏭️  Форма уже существует")


def main():
    """Главная функция"""
    print("\n" + "="*80)
    print("🚀 SETUP FONON JEWELRY RETAIL DATA COLLECTION SYSTEM")
    print("="*80 + "\n")

    categories = setup_categories()
    setup_attributes(categories)
    coefficients = setup_coefficients()
    formulas = setup_formulas(coefficients)
    setup_metrics(coefficients, formulas)
    setup_form_templates(coefficients)

    print("\n" + "="*80)
    print("✅ ЗАВЕРШЕНО! Система FONON полностью настроена.")
    print("="*80 + "\n")

    print("📋 Что было создано:")
    print(f"   • {Category.objects.count()} категорий изделий")
    print(f"   • {AttributeGroup.objects.count()} групп атрибутов")
    print(f"   • {AttributeDefinition.objects.count()} атрибутов")
    print(f"   • {Coefficient.objects.count()} коэффициентов")
    print(f"   • {Formula.objects.count()} формул")
    print(f"   • {Metric.objects.count()} метрик")
    print(f"   • {FormTemplate.objects.count()} шаблонов форм")

    print("\n📌 Следующие шаги:")
    print("   1. Создать тип визита и привязать форму 'FONON - Мониторинг ювелирного магазина'")
    print("   2. Назначить визиты полевым сотрудникам")
    print("   3. Создать дашборды для аналитики")
    print("\n")


if __name__ == '__main__':
    main()
