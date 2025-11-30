"""
Django management command to setup FONON jewelry retail data collection system
Usage: python manage.py setup_fonon
"""

from django.core.management.base import BaseCommand
from catalog.models import Category, AttributeGroup, AttributeDefinition
from coefficients.models import Coefficient, Metric, Formula
from forms.models import FormTemplate
import json


class Command(BaseCommand):
    help = 'Setup FONON jewelry retail data collection system'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*80)
        self.stdout.write(self.style.SUCCESS("SETUP FONON JEWELRY RETAIL DATA COLLECTION SYSTEM"))
        self.stdout.write("="*80 + "\n")

        self.setup_categories()
        categories = Category.objects.filter(code__in=['rings', 'earrings', 'chains', 'bracelets', 'pendants', 'sets'])
        self.setup_attributes(categories)
        coefficients = self.setup_coefficients()
        formulas = self.setup_formulas(coefficients)
        self.setup_metrics(coefficients, formulas)
        self.setup_form_templates(coefficients)

        self.stdout.write("\n" + "="*80)
        self.stdout.write(self.style.SUCCESS("COMPLETED! FONON system fully configured."))
        self.stdout.write("="*80 + "\n")

        self.stdout.write("\nWhat was created:")
        self.stdout.write(f"   - {Category.objects.count()} product categories")
        self.stdout.write(f"   - {AttributeGroup.objects.count()} attribute groups")
        self.stdout.write(f"   - {AttributeDefinition.objects.count()} attributes")
        self.stdout.write(f"   - {Coefficient.objects.count()} coefficients")
        self.stdout.write(f"   - {Formula.objects.count()} formulas")
        self.stdout.write(f"   - {Metric.objects.count()} metrics")
        self.stdout.write(f"   - {FormTemplate.objects.count()} form templates")

        self.stdout.write("\nNext steps:")
        self.stdout.write("   1. Create visit type and attach 'FONON - Jewelry Monitoring' form")
        self.stdout.write("   2. Assign visits to field staff")
        self.stdout.write("   3. Create dashboards for analytics\n")

    def setup_categories(self):
        """Create jewelry product categories"""
        self.stdout.write("Creating categories...")

        categories_data = [
            {'name': 'Кольца', 'code': 'rings'},
            {'name': 'Серьги', 'code': 'earrings'},
            {'name': 'Цепочки', 'code': 'chains'},
            {'name': 'Браслеты', 'code': 'bracelets'},
            {'name': 'Кулоны', 'code': 'pendants'},
            {'name': 'Комплекты', 'code': 'sets'},
        ]

        for data in categories_data:
            cat, created = Category.objects.get_or_create(
                code=data['code'],
                defaults={'name': data['name']}
            )
            if created:
                self.stdout.write(f"   [+] {cat.name}")
            else:
                self.stdout.write(f"   [=] {cat.name} (already exists)")

    def setup_attributes(self, categories):
        """Create attributes for jewelry products"""
        self.stdout.write("\nCreating attribute groups...")

        for category in categories:
            # Metal group
            metal_group, created = AttributeGroup.objects.get_or_create(
                code=f'metal_{category.code}',
                category=category,
                defaults={'name': 'Металл', 'order': 1}
            )
            if created:
                self.stdout.write(f"   [+] Metal group for {category.name}")

            # Stones group
            stones_group, created = AttributeGroup.objects.get_or_create(
                code=f'stones_{category.code}',
                category=category,
                defaults={'name': 'Камни', 'order': 2}
            )
            if created:
                self.stdout.write(f"   [+] Stones group for {category.name}")

    def setup_coefficients(self):
        """Create all coefficients"""
        self.stdout.write("\nCreating coefficients...")

        coefficients_data = [
            # 1. Passability
            {'name': 'Проходимость', 'code': 'passability', 'unit': 'чел./час', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            # 2. Counter count
            {'name': 'Количество прилавков', 'code': 'counter_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            # 3-4. Products
            {'name': 'Всего изделий в магазине', 'code': 'total_products_store', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Изделий на прилавке', 'code': 'products_per_counter', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            # 5. Premium
            {'name': 'Количество премиум изделий', 'code': 'premium_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            # 6-8. Metal types
            {'name': 'Изделия из желтого золота', 'code': 'yellow_gold_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Изделия из красного золота', 'code': 'red_gold_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Изделия из белого золота', 'code': 'white_gold_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            # 9-13. Categories (count)
            {'name': 'Количество колец', 'code': 'rings_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Количество серег', 'code': 'earrings_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Количество цепочек', 'code': 'chains_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Количество браслетов', 'code': 'bracelets_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Количество кулонов', 'code': 'pendants_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            # 14-18. Weights
            {'name': 'Суммарный вес колец', 'code': 'rings_total_weight', 'unit': 'гр', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Суммарный вес серег', 'code': 'earrings_total_weight', 'unit': 'гр', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Суммарный вес цепочек', 'code': 'chains_total_weight', 'unit': 'гр', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Суммарный вес браслетов', 'code': 'bracelets_total_weight', 'unit': 'гр', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Суммарный вес кулонов', 'code': 'pendants_total_weight', 'unit': 'гр', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            # 19-20. Sets
            {'name': 'Количество комплектов', 'code': 'sets_count', 'unit': 'шт', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            {'name': 'Суммарный вес комплектов', 'code': 'sets_total_weight', 'unit': 'гр', 'value_type': 'numeric', 'data_type': 'MON', 'applies_to_outlet': True},
            # 21. Sales
            {'name': 'Продаж в час', 'code': 'sales_per_hour', 'unit': 'шт/час', 'value_type': 'numeric', 'data_type': 'EXP', 'applies_to_outlet': True},
            {'name': 'Продаж в день', 'code': 'sales_per_day', 'unit': 'шт/день', 'value_type': 'numeric', 'data_type': 'EXP', 'applies_to_outlet': True},
            # Sales by category
            {'name': 'Продажи колец в день', 'code': 'rings_sales_per_day', 'unit': 'шт/день', 'value_type': 'numeric', 'data_type': 'EXP', 'applies_to_outlet': True},
            {'name': 'Продажи серег в день', 'code': 'earrings_sales_per_day', 'unit': 'шт/день', 'value_type': 'numeric', 'data_type': 'EXP', 'applies_to_outlet': True},
            {'name': 'Продажи цепочек в день', 'code': 'chains_sales_per_day', 'unit': 'шт/день', 'value_type': 'numeric', 'data_type': 'EXP', 'applies_to_outlet': True},
            {'name': 'Продажи браслетов в день', 'code': 'bracelets_sales_per_day', 'unit': 'шт/день', 'value_type': 'numeric', 'data_type': 'EXP', 'applies_to_outlet': True},
            {'name': 'Продажи кулонов в день', 'code': 'pendants_sales_per_day', 'unit': 'шт/день', 'value_type': 'numeric', 'data_type': 'EXP', 'applies_to_outlet': True},
        ]

        created_coefficients = {}
        for data in coefficients_data:
            coef, created = Coefficient.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            created_coefficients[data['code']] = coef
            if created:
                self.stdout.write(f"   [+] {coef.name}")

        return created_coefficients

    def setup_formulas(self, coefficients):
        """Create formulas for calculated metrics"""
        self.stdout.write("\nCreating formulas...")

        formulas_data = [
            {'name': 'Доля премиум сегмента', 'code': 'premium_share', 'expression': '(C1 / C2) * 100', 'coefficient_map': {'C1': 'premium_count', 'C2': 'total_products_store'}},
            {'name': 'Доля желтого золота', 'code': 'yellow_gold_share', 'expression': '(C1 / C2) * 100', 'coefficient_map': {'C1': 'yellow_gold_count', 'C2': 'total_products_store'}},
            {'name': 'Доля красного золота', 'code': 'red_gold_share', 'expression': '(C1 / C2) * 100', 'coefficient_map': {'C1': 'red_gold_count', 'C2': 'total_products_store'}},
            {'name': 'Доля белого золота', 'code': 'white_gold_share', 'expression': '(C1 / C2) * 100', 'coefficient_map': {'C1': 'white_gold_count', 'C2': 'total_products_store'}},
            {'name': 'Средний вес кольца', 'code': 'avg_ring_weight', 'expression': 'C1 / C2', 'coefficient_map': {'C1': 'rings_total_weight', 'C2': 'rings_count'}},
            {'name': 'Средний вес серег', 'code': 'avg_earring_weight', 'expression': 'C1 / C2', 'coefficient_map': {'C1': 'earrings_total_weight', 'C2': 'earrings_count'}},
            {'name': 'Средний вес цепочки', 'code': 'avg_chain_weight', 'expression': 'C1 / C2', 'coefficient_map': {'C1': 'chains_total_weight', 'C2': 'chains_count'}},
            {'name': 'Средний вес браслета', 'code': 'avg_bracelet_weight', 'expression': 'C1 / C2', 'coefficient_map': {'C1': 'bracelets_total_weight', 'C2': 'bracelets_count'}},
            {'name': 'Средний вес кулона', 'code': 'avg_pendant_weight', 'expression': 'C1 / C2', 'coefficient_map': {'C1': 'pendants_total_weight', 'C2': 'pendants_count'}},
            {'name': 'Средний вес комплекта', 'code': 'avg_set_weight', 'expression': 'C1 / C2', 'coefficient_map': {'C1': 'sets_total_weight', 'C2': 'sets_count'}},
        ]

        created_formulas = {}
        for data in formulas_data:
            # Get coefficient objects
            coef_objs = []
            for placeholder, code in data['coefficient_map'].items():
                if code in coefficients:
                    coef_objs.append(coefficients[code])

            formula, created = Formula.objects.get_or_create(
                code=data['code'],
                defaults={
                    'name': data['name'],
                    'expression': data['expression'],
                }
            )

            # Add coefficients to formula
            if created and coef_objs:
                formula.coefficients.set(coef_objs)

            created_formulas[data['code']] = formula
            if created:
                self.stdout.write(f"   [+] {formula.name}")

        return created_formulas

    def setup_metrics(self, coefficients, formulas):
        """Create metrics"""
        self.stdout.write("\nCreating metrics...")

        metrics_data = [
            {'name': 'Доля премиум сегмента', 'code': 'premium_share_metric', 'category': 'share', 'formula': 'premium_share', 'unit': '%', 'target_value': 25.0},
            {'name': 'Доля желтого золота', 'code': 'yellow_gold_share_metric', 'category': 'share', 'formula': 'yellow_gold_share', 'unit': '%'},
            {'name': 'Доля красного золота', 'code': 'red_gold_share_metric', 'category': 'share', 'formula': 'red_gold_share', 'unit': '%'},
            {'name': 'Доля белого золота', 'code': 'white_gold_share_metric', 'category': 'share', 'formula': 'white_gold_share', 'unit': '%'},
            {'name': 'Средний вес кольца', 'code': 'avg_ring_weight_metric', 'category': 'other', 'formula': 'avg_ring_weight', 'unit': 'гр'},
            {'name': 'Средний вес серег', 'code': 'avg_earring_weight_metric', 'category': 'other', 'formula': 'avg_earring_weight', 'unit': 'гр'},
            {'name': 'Средний вес цепочки', 'code': 'avg_chain_weight_metric', 'category': 'other', 'formula': 'avg_chain_weight', 'unit': 'гр'},
            {'name': 'Средний вес браслета', 'code': 'avg_bracelet_weight_metric', 'category': 'other', 'formula': 'avg_bracelet_weight', 'unit': 'гр'},
            {'name': 'Средний вес кулона', 'code': 'avg_pendant_weight_metric', 'category': 'other', 'formula': 'avg_pendant_weight', 'unit': 'гр'},
            {'name': 'Средний вес комплекта', 'code': 'avg_set_weight_metric', 'category': 'other', 'formula': 'avg_set_weight', 'unit': 'гр'},
        ]

        for data in metrics_data:
            formula_obj = formulas.get(data.get('formula')) if data.get('formula') else None
            metric, created = Metric.objects.get_or_create(
                code=data['code'],
                defaults={
                    'name': data['name'],
                    'category': data['category'],
                    'formula': formula_obj,
                }
            )
            if created:
                self.stdout.write(f"   [+] {metric.name}")

    def setup_form_templates(self, coefficients):
        """Create form templates for visits"""
        self.stdout.write("\nCreating form templates...")

        form_template, created = FormTemplate.objects.get_or_create(
            code='fonon_jewelry_monitoring',
            defaults={
                'name': 'FONON - Monitoring yuvelirnogo magazina',
                'description': 'Complete form for jewelry retail data collection',
                'form_type': 'visit',
                'fields_schema': [],  # Schema will be filled separately
                'category': 'jewelry',
                'status': 'active',
            }
        )

        if created:
            self.stdout.write("   [+] Form template created")
        else:
            self.stdout.write("   [=] Form template already exists")
