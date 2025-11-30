from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from analytics.models import Dashboard
from coefficients.models import Coefficient
import json

User = get_user_model()


class Command(BaseCommand):
    help = 'Create FONON sample dashboard with key jewelry metrics'

    def handle(self, *args, **options):
        self.stdout.write("="*80)
        self.stdout.write("CREATE FONON SAMPLE DASHBOARD")
        self.stdout.write("="*80)

        # Get or create admin user
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                self.stdout.write(self.style.WARNING("No admin user found, using first user..."))
                admin_user = User.objects.first()

            if not admin_user:
                self.stdout.write(self.style.ERROR("ERROR: No users in system!"))
                return

            self.stdout.write(f"Using user: {admin_user.username}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"ERROR finding user: {e}"))
            return

        # Get coefficient IDs (using actual codes from setup_fonon)
        coefficients = {}
        coef_codes = [
            'passability', 'counter_count', 'total_products_store', 'products_per_counter',
            'premium_count', 'yellow_gold_count', 'red_gold_count', 'white_gold_count',
            'rings_count', 'earrings_count', 'chains_count', 'bracelets_count', 'pendants_count', 'sets_count',
            'rings_total_weight', 'earrings_total_weight', 'chains_total_weight',
            'bracelets_total_weight', 'pendants_total_weight', 'sets_total_weight',
            'rings_sales_per_day', 'earrings_sales_per_day', 'chains_sales_per_day',
            'bracelets_sales_per_day', 'pendants_sales_per_day'
        ]

        for code in coef_codes:
            try:
                coef = Coefficient.objects.get(code=code)
                coefficients[code] = coef.id
            except Coefficient.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"WARNING: Coefficient '{code}' not found"))

        if not coefficients:
            self.stdout.write(self.style.ERROR("ERROR: No coefficients found! Run setup_fonon first."))
            return

        # Build dashboard configuration
        widgets_config = {
            "widgets": [
                # Row 1: Key metrics
                {
                    "type": "metric",
                    "title": "Проходимость",
                    "coefficient_id": coefficients.get('passability'),
                    "aggregation": "avg",
                    "unit": "чел/час",
                    "color": "primary"
                },
                {
                    "type": "metric",
                    "title": "Прилавков в среднем",
                    "coefficient_id": coefficients.get('counter_count'),
                    "aggregation": "avg",
                    "unit": "шт",
                    "color": "info"
                },
                {
                    "type": "metric",
                    "title": "Изделий в магазине",
                    "coefficient_id": coefficients.get('total_products_store'),
                    "aggregation": "avg",
                    "unit": "шт",
                    "color": "success"
                },
                {
                    "type": "metric",
                    "title": "Премиум сегмент",
                    "coefficient_id": coefficients.get('premium_count'),
                    "aggregation": "avg",
                    "unit": "шт",
                    "color": "warning"
                },

                # Row 2: Metal distribution chart
                {
                    "type": "chart",
                    "title": "Распределение по металлам (желтое золото)",
                    "chart_type": "bar",
                    "coefficient_id": coefficients.get('yellow_gold_count'),
                    "group_by": "channel",
                    "color": "rgba(255, 205, 86, 0.8)"
                },

                # Row 2: Category distribution chart
                {
                    "type": "chart",
                    "title": "Распределение по категориям (кольца)",
                    "chart_type": "bar",
                    "coefficient_id": coefficients.get('rings_count'),
                    "group_by": "channel",
                    "color": "rgba(54, 162, 235, 0.8)"
                },

                # Row 3: Trend charts
                {
                    "type": "chart",
                    "title": "Динамика проходимости",
                    "chart_type": "line",
                    "coefficient_id": coefficients.get('passability'),
                    "group_by": "date",
                    "color": "rgba(75, 192, 192, 0.8)"
                },

                {
                    "type": "chart",
                    "title": "Динамика ассортимента",
                    "chart_type": "line",
                    "coefficient_id": coefficients.get('total_products_store'),
                    "group_by": "date",
                    "color": "rgba(153, 102, 255, 0.8)"
                },

                # Row 4: Regional distribution
                {
                    "type": "chart",
                    "title": "Проходимость по регионам",
                    "chart_type": "bar",
                    "coefficient_id": coefficients.get('passability'),
                    "group_by": "region",
                    "color": "rgba(255, 99, 132, 0.8)"
                },

                {
                    "type": "chart",
                    "title": "Ассортимент по каналам",
                    "chart_type": "bar",
                    "coefficient_id": coefficients.get('total_products_store'),
                    "group_by": "channel",
                    "color": "rgba(255, 159, 64, 0.8)"
                }
            ]
        }

        # Create dashboard
        dashboard, created = Dashboard.objects.get_or_create(
            code='fonon_jewelry_dashboard',
            defaults={
                'name': 'FONON - Мониторинг ювелирного рынка',
                'description': 'Комплексный дашборд для отслеживания ключевых метрик ювелирных магазинов: проходимость, ассортимент, распределение по металлам и категориям',
                'dashboard_type': 'operational',
                'widgets_config': widgets_config,
                'owner': admin_user,
                'is_public': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"\nSUCCESS! Created dashboard: {dashboard.name}"))
            self.stdout.write(f"Dashboard ID: {dashboard.id}")
            self.stdout.write(f"Dashboard code: {dashboard.code}")
            self.stdout.write(f"Widgets configured: {len(widgets_config['widgets'])}")
        else:
            # Update existing dashboard
            dashboard.widgets_config = widgets_config
            dashboard.save()
            self.stdout.write(self.style.SUCCESS(f"\nUPDATED existing dashboard: {dashboard.name}"))

        self.stdout.write("\nWidget types:")
        metrics = sum(1 for w in widgets_config['widgets'] if w['type'] == 'metric')
        charts = sum(1 for w in widgets_config['widgets'] if w['type'] == 'chart')
        self.stdout.write(f"  - Metrics: {metrics}")
        self.stdout.write(f"  - Charts: {charts}")

        self.stdout.write("\nChart types:")
        chart_types = {}
        for w in widgets_config['widgets']:
            if w['type'] == 'chart':
                ct = w.get('chart_type', 'line')
                chart_types[ct] = chart_types.get(ct, 0) + 1

        for ct, count in chart_types.items():
            self.stdout.write(f"  - {ct}: {count}")

        self.stdout.write("\n" + "="*80)
        self.stdout.write(f"Dashboard URL: /analytics/dashboards/{dashboard.id}/")
        self.stdout.write("="*80)
