"""
Management command для настройки метрик мониторинга ювелирных изделий

Создает 21 метрику для отслеживания:
1. Проходимость (чел./час)
2. Количество магазинов (прилавков)
3. Количество изделий в магазине
4. Количество изделий на прилавке
5. Доля изделий премиум сегмента (с драгоценными камнями) в %
6. Доля изделий из желтого золота в %
7. Доля изделий из красного золота в %
8. Доля изделий из белого золота в %
9. Количество колец
10. Количество серег
11. Количество цепей (цепочек)
12. Количество цепей (браслетов)
13. Количество кулонов
14. Средний вес колец (гр.)
15. Средний вес серег (гр.)
16. Средний вес цепей (цепочек) (гр.)
17. Средний вес цепей (браслетов) (гр.)
18. Средний вес кулонов (гр.)
19. Количество комплектов
20. Средний вес комплектов
21. Количество продаж магазина(прилавка)(при возможности разбиение по категориям/типам изделий) в час, в день
"""

from django.core.management.base import BaseCommand
from coefficients.models import Coefficient, Formula, Metric


class Command(BaseCommand):
    help = 'Настройка метрик для мониторинга ювелирных изделий (21 показатель)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('НАСТРОЙКА МЕТРИК МОНИТОРИНГА ЮВЕЛИРНЫХ ИЗДЕЛИЙ'))
        self.stdout.write(self.style.SUCCESS('=' * 70))

        # ====================================================================
        # БАЗОВЫЕ КОЭФФИЦИЕНТЫ (прямые замеры)
        # ====================================================================

        base_coefficients = [
            # 1. Проходимость
            {
                'name': 'Проходимость магазина',
                'code': 'traffic_per_hour',
                'description': 'Количество посетителей, проходящих мимо/через магазин в час',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'чел./час',
                'applies_to_outlet': True,
            },

            # 2. Количество магазинов (прилавков)
            {
                'name': 'Количество прилавков',
                'code': 'counter_count',
                'description': 'Количество прилавков/витрин в торговой точке',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },

            # 3. Количество изделий в магазине
            {
                'name': 'Общее количество изделий в магазине',
                'code': 'total_items_store',
                'description': 'Общее количество ювелирных изделий в торговой точке',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },

            # 4. Количество изделий на прилавке
            {
                'name': 'Количество изделий на прилавке',
                'code': 'items_per_counter',
                'description': 'Количество изделий на одном прилавке/витрине',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },

            # 5. Количество изделий премиум сегмента
            {
                'name': 'Количество изделий с драгоценными камнями',
                'code': 'premium_items_count',
                'description': 'Количество изделий премиум сегмента (с драгоценными камнями)',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },

            # 6-8. Количество изделий по цвету металла
            {
                'name': 'Количество изделий из желтого золота',
                'code': 'yellow_gold_count',
                'description': 'Количество изделий из желтого золота',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },
            {
                'name': 'Количество изделий из красного золота',
                'code': 'red_gold_count',
                'description': 'Количество изделий из красного золота',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },
            {
                'name': 'Количество изделий из белого золота',
                'code': 'white_gold_count',
                'description': 'Количество изделий из белого золота',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },

            # 9-13. Количество по типам изделий
            {
                'name': 'Количество колец',
                'code': 'rings_count',
                'description': 'Количество колец в торговой точке',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },
            {
                'name': 'Количество серег',
                'code': 'earrings_count',
                'description': 'Количество серег в торговой точке',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },
            {
                'name': 'Количество цепочек',
                'code': 'chains_count',
                'description': 'Количество цепочек в торговой точке',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },
            {
                'name': 'Количество браслетов',
                'code': 'bracelets_count',
                'description': 'Количество браслетов в торговой точке',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },
            {
                'name': 'Количество кулонов',
                'code': 'pendants_count',
                'description': 'Количество кулонов/подвесок в торговой точке',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },

            # 14-18. Суммарный вес по типам изделий (для расчета среднего)
            {
                'name': 'Суммарный вес колец',
                'code': 'rings_total_weight',
                'description': 'Суммарный вес всех колец в граммах',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'г',
                'applies_to_outlet': True,
            },
            {
                'name': 'Суммарный вес серег',
                'code': 'earrings_total_weight',
                'description': 'Суммарный вес всех серег в граммах',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'г',
                'applies_to_outlet': True,
            },
            {
                'name': 'Суммарный вес цепочек',
                'code': 'chains_total_weight',
                'description': 'Суммарный вес всех цепочек в граммах',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'г',
                'applies_to_outlet': True,
            },
            {
                'name': 'Суммарный вес браслетов',
                'code': 'bracelets_total_weight',
                'description': 'Суммарный вес всех браслетов в граммах',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'г',
                'applies_to_outlet': True,
            },
            {
                'name': 'Суммарный вес кулонов',
                'code': 'pendants_total_weight',
                'description': 'Суммарный вес всех кулонов в граммах',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'г',
                'applies_to_outlet': True,
            },

            # 19-20. Комплекты
            {
                'name': 'Количество комплектов',
                'code': 'sets_count',
                'description': 'Количество комплектов ювелирных изделий',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт',
                'applies_to_outlet': True,
            },
            {
                'name': 'Суммарный вес комплектов',
                'code': 'sets_total_weight',
                'description': 'Суммарный вес всех комплектов в граммах',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'г',
                'applies_to_outlet': True,
            },

            # 21. Продажи
            {
                'name': 'Количество продаж в час',
                'code': 'sales_per_hour',
                'description': 'Количество продаж в час',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт/час',
                'applies_to_outlet': True,
            },
            {
                'name': 'Количество продаж в день',
                'code': 'sales_per_day',
                'description': 'Количество продаж в день',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт/день',
                'applies_to_outlet': True,
            },

            # Продажи по категориям
            {
                'name': 'Продажи колец в день',
                'code': 'rings_sales_per_day',
                'description': 'Количество проданных колец в день',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт/день',
                'applies_to_outlet': True,
            },
            {
                'name': 'Продажи серег в день',
                'code': 'earrings_sales_per_day',
                'description': 'Количество проданных серег в день',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт/день',
                'applies_to_outlet': True,
            },
            {
                'name': 'Продажи цепочек в день',
                'code': 'chains_sales_per_day',
                'description': 'Количество проданных цепочек в день',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт/день',
                'applies_to_outlet': True,
            },
            {
                'name': 'Продажи браслетов в день',
                'code': 'bracelets_sales_per_day',
                'description': 'Количество проданных браслетов в день',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт/день',
                'applies_to_outlet': True,
            },
            {
                'name': 'Продажи кулонов в день',
                'code': 'pendants_sales_per_day',
                'description': 'Количество проданных кулонов в день',
                'data_type': 'MON',
                'value_type': 'numeric',
                'unit': 'шт/день',
                'applies_to_outlet': True,
            },
        ]

        self.stdout.write('\n[1/3] Создание базовых коэффициентов...')
        self.stdout.write('-' * 70)

        coefficients_map = {}
        for coeff_data in base_coefficients:
            coeff, created = Coefficient.objects.get_or_create(
                code=coeff_data['code'],
                defaults=coeff_data
            )
            coefficients_map[coeff_data['code']] = coeff

            if created:
                self.stdout.write(self.style.SUCCESS(f'  [+] Создан: {coeff.name}'))
            else:
                self.stdout.write(f'  [-] Существует: {coeff.name}')

        # ====================================================================
        # ФОРМУЛЫ ДЛЯ РАСЧЕТНЫХ МЕТРИК
        # ====================================================================

        formulas_data = [
            # Доля премиум сегмента
            {
                'name': 'Доля изделий премиум сегмента',
                'code': 'premium_share_formula',
                'description': 'Процент изделий с драгоценными камнями от общего количества',
                'expression': '(premium_items_count / total_items_store) * 100',
                'source_data_type': 'MON',
                'result_type': 'percentage',
                'result_unit': '%',
                'coefficients_codes': ['premium_items_count', 'total_items_store'],
            },

            # Доли по цвету золота
            {
                'name': 'Доля изделий из желтого золота',
                'code': 'yellow_gold_share_formula',
                'description': 'Процент изделий из желтого золота',
                'expression': '(yellow_gold_count / total_items_store) * 100',
                'source_data_type': 'MON',
                'result_type': 'percentage',
                'result_unit': '%',
                'coefficients_codes': ['yellow_gold_count', 'total_items_store'],
            },
            {
                'name': 'Доля изделий из красного золота',
                'code': 'red_gold_share_formula',
                'description': 'Процент изделий из красного золота',
                'expression': '(red_gold_count / total_items_store) * 100',
                'source_data_type': 'MON',
                'result_type': 'percentage',
                'result_unit': '%',
                'coefficients_codes': ['red_gold_count', 'total_items_store'],
            },
            {
                'name': 'Доля изделий из белого золота',
                'code': 'white_gold_share_formula',
                'description': 'Процент изделий из белого золота',
                'expression': '(white_gold_count / total_items_store) * 100',
                'source_data_type': 'MON',
                'result_type': 'percentage',
                'result_unit': '%',
                'coefficients_codes': ['white_gold_count', 'total_items_store'],
            },

            # Средние веса
            {
                'name': 'Средний вес колец',
                'code': 'rings_avg_weight_formula',
                'description': 'Средний вес одного кольца',
                'expression': 'rings_total_weight / rings_count',
                'source_data_type': 'MON',
                'result_type': 'numeric',
                'result_unit': 'г',
                'coefficients_codes': ['rings_total_weight', 'rings_count'],
            },
            {
                'name': 'Средний вес серег',
                'code': 'earrings_avg_weight_formula',
                'description': 'Средний вес одной пары серег',
                'expression': 'earrings_total_weight / earrings_count',
                'source_data_type': 'MON',
                'result_type': 'numeric',
                'result_unit': 'г',
                'coefficients_codes': ['earrings_total_weight', 'earrings_count'],
            },
            {
                'name': 'Средний вес цепочек',
                'code': 'chains_avg_weight_formula',
                'description': 'Средний вес одной цепочки',
                'expression': 'chains_total_weight / chains_count',
                'source_data_type': 'MON',
                'result_type': 'numeric',
                'result_unit': 'г',
                'coefficients_codes': ['chains_total_weight', 'chains_count'],
            },
            {
                'name': 'Средний вес браслетов',
                'code': 'bracelets_avg_weight_formula',
                'description': 'Средний вес одного браслета',
                'expression': 'bracelets_total_weight / bracelets_count',
                'source_data_type': 'MON',
                'result_type': 'numeric',
                'result_unit': 'г',
                'coefficients_codes': ['bracelets_total_weight', 'bracelets_count'],
            },
            {
                'name': 'Средний вес кулонов',
                'code': 'pendants_avg_weight_formula',
                'description': 'Средний вес одного кулона',
                'expression': 'pendants_total_weight / pendants_count',
                'source_data_type': 'MON',
                'result_type': 'numeric',
                'result_unit': 'г',
                'coefficients_codes': ['pendants_total_weight', 'pendants_count'],
            },
            {
                'name': 'Средний вес комплектов',
                'code': 'sets_avg_weight_formula',
                'description': 'Средний вес одного комплекта',
                'expression': 'sets_total_weight / sets_count',
                'source_data_type': 'MON',
                'result_type': 'numeric',
                'result_unit': 'г',
                'coefficients_codes': ['sets_total_weight', 'sets_count'],
            },
        ]

        self.stdout.write('\n[2/3] Создание формул для расчетных метрик...')
        self.stdout.write('-' * 70)

        formulas_map = {}
        for formula_data in formulas_data:
            coefficients_codes = formula_data.pop('coefficients_codes', [])
            formula, created = Formula.objects.get_or_create(
                code=formula_data['code'],
                defaults=formula_data
            )
            formulas_map[formula_data['code']] = formula

            # Связываем коэффициенты с формулой
            for coeff_code in coefficients_codes:
                if coeff_code in coefficients_map:
                    formula.coefficients.add(coefficients_map[coeff_code])

            if created:
                self.stdout.write(self.style.SUCCESS(f'  [+] Создана: {formula.name}'))
            else:
                self.stdout.write(f'  [-] Существует: {formula.name}')

        # ====================================================================
        # МЕТРИКИ (ФИНАЛЬНЫЕ ПОКАЗАТЕЛИ)
        # ====================================================================

        metrics_data = [
            # Прямые метрики (из коэффициентов)
            {
                'name': '1. Проходимость (чел./час)',
                'code': 'metric_traffic_per_hour',
                'description': 'Количество посетителей в час',
                'category': 'other',
                'source_data_type': 'MON',
                'coefficients_codes': ['traffic_per_hour'],
            },
            {
                'name': '2. Количество прилавков',
                'code': 'metric_counter_count',
                'description': 'Количество прилавков в магазине',
                'category': 'other',
                'source_data_type': 'MON',
                'coefficients_codes': ['counter_count'],
            },
            {
                'name': '3. Количество изделий в магазине',
                'code': 'metric_total_items_store',
                'description': 'Общее количество изделий в торговой точке',
                'category': 'availability',
                'source_data_type': 'MON',
                'coefficients_codes': ['total_items_store'],
            },
            {
                'name': '4. Количество изделий на прилавке',
                'code': 'metric_items_per_counter',
                'description': 'Среднее количество изделий на прилавке',
                'category': 'availability',
                'source_data_type': 'MON',
                'coefficients_codes': ['items_per_counter'],
            },
            {
                'name': '5. Доля изделий премиум сегмента (%)',
                'code': 'metric_premium_share',
                'description': 'Процент изделий с драгоценными камнями',
                'category': 'share',
                'source_data_type': 'MON',
                'formula_code': 'premium_share_formula',
                'coefficients_codes': ['premium_items_count', 'total_items_store'],
            },
            {
                'name': '6. Доля изделий из желтого золота (%)',
                'code': 'metric_yellow_gold_share',
                'description': 'Процент изделий из желтого золота',
                'category': 'share',
                'source_data_type': 'MON',
                'formula_code': 'yellow_gold_share_formula',
                'coefficients_codes': ['yellow_gold_count', 'total_items_store'],
            },
            {
                'name': '7. Доля изделий из красного золота (%)',
                'code': 'metric_red_gold_share',
                'description': 'Процент изделий из красного золота',
                'category': 'share',
                'source_data_type': 'MON',
                'formula_code': 'red_gold_share_formula',
                'coefficients_codes': ['red_gold_count', 'total_items_store'],
            },
            {
                'name': '8. Доля изделий из белого золота (%)',
                'code': 'metric_white_gold_share',
                'description': 'Процент изделий из белого золота',
                'category': 'share',
                'source_data_type': 'MON',
                'formula_code': 'white_gold_share_formula',
                'coefficients_codes': ['white_gold_count', 'total_items_store'],
            },
            {
                'name': '9. Количество колец',
                'code': 'metric_rings_count',
                'description': 'Количество колец в наличии',
                'category': 'availability',
                'source_data_type': 'MON',
                'coefficients_codes': ['rings_count'],
            },
            {
                'name': '10. Количество серег',
                'code': 'metric_earrings_count',
                'description': 'Количество серег в наличии',
                'category': 'availability',
                'source_data_type': 'MON',
                'coefficients_codes': ['earrings_count'],
            },
            {
                'name': '11. Количество цепочек',
                'code': 'metric_chains_count',
                'description': 'Количество цепочек в наличии',
                'category': 'availability',
                'source_data_type': 'MON',
                'coefficients_codes': ['chains_count'],
            },
            {
                'name': '12. Количество браслетов',
                'code': 'metric_bracelets_count',
                'description': 'Количество браслетов в наличии',
                'category': 'availability',
                'source_data_type': 'MON',
                'coefficients_codes': ['bracelets_count'],
            },
            {
                'name': '13. Количество кулонов',
                'code': 'metric_pendants_count',
                'description': 'Количество кулонов в наличии',
                'category': 'availability',
                'source_data_type': 'MON',
                'coefficients_codes': ['pendants_count'],
            },
            {
                'name': '14. Средний вес колец (гр.)',
                'code': 'metric_rings_avg_weight',
                'description': 'Средний вес одного кольца',
                'category': 'other',
                'source_data_type': 'MON',
                'formula_code': 'rings_avg_weight_formula',
                'coefficients_codes': ['rings_total_weight', 'rings_count'],
            },
            {
                'name': '15. Средний вес серег (гр.)',
                'code': 'metric_earrings_avg_weight',
                'description': 'Средний вес одной пары серег',
                'category': 'other',
                'source_data_type': 'MON',
                'formula_code': 'earrings_avg_weight_formula',
                'coefficients_codes': ['earrings_total_weight', 'earrings_count'],
            },
            {
                'name': '16. Средний вес цепочек (гр.)',
                'code': 'metric_chains_avg_weight',
                'description': 'Средний вес одной цепочки',
                'category': 'other',
                'source_data_type': 'MON',
                'formula_code': 'chains_avg_weight_formula',
                'coefficients_codes': ['chains_total_weight', 'chains_count'],
            },
            {
                'name': '17. Средний вес браслетов (гр.)',
                'code': 'metric_bracelets_avg_weight',
                'description': 'Средний вес одного браслета',
                'category': 'other',
                'source_data_type': 'MON',
                'formula_code': 'bracelets_avg_weight_formula',
                'coefficients_codes': ['bracelets_total_weight', 'bracelets_count'],
            },
            {
                'name': '18. Средний вес кулонов (гр.)',
                'code': 'metric_pendants_avg_weight',
                'description': 'Средний вес одного кулона',
                'category': 'other',
                'source_data_type': 'MON',
                'formula_code': 'pendants_avg_weight_formula',
                'coefficients_codes': ['pendants_total_weight', 'pendants_count'],
            },
            {
                'name': '19. Количество комплектов',
                'code': 'metric_sets_count',
                'description': 'Количество комплектов в наличии',
                'category': 'availability',
                'source_data_type': 'MON',
                'coefficients_codes': ['sets_count'],
            },
            {
                'name': '20. Средний вес комплектов (гр.)',
                'code': 'metric_sets_avg_weight',
                'description': 'Средний вес одного комплекта',
                'category': 'other',
                'source_data_type': 'MON',
                'formula_code': 'sets_avg_weight_formula',
                'coefficients_codes': ['sets_total_weight', 'sets_count'],
            },
            {
                'name': '21. Продажи в час',
                'code': 'metric_sales_per_hour',
                'description': 'Количество продаж в час',
                'category': 'other',
                'source_data_type': 'MON',
                'coefficients_codes': ['sales_per_hour'],
            },
            {
                'name': '21. Продажи в день',
                'code': 'metric_sales_per_day',
                'description': 'Количество продаж в день',
                'category': 'other',
                'source_data_type': 'MON',
                'coefficients_codes': ['sales_per_day'],
            },

            # Продажи по категориям
            {
                'name': '21.1 Продажи колец в день',
                'code': 'metric_rings_sales',
                'description': 'Количество проданных колец в день',
                'category': 'other',
                'source_data_type': 'MON',
                'coefficients_codes': ['rings_sales_per_day'],
            },
            {
                'name': '21.2 Продажи серег в день',
                'code': 'metric_earrings_sales',
                'description': 'Количество проданных серег в день',
                'category': 'other',
                'source_data_type': 'MON',
                'coefficients_codes': ['earrings_sales_per_day'],
            },
            {
                'name': '21.3 Продажи цепочек в день',
                'code': 'metric_chains_sales',
                'description': 'Количество проданных цепочек в день',
                'category': 'other',
                'source_data_type': 'MON',
                'coefficients_codes': ['chains_sales_per_day'],
            },
            {
                'name': '21.4 Продажи браслетов в день',
                'code': 'metric_bracelets_sales',
                'description': 'Количество проданных браслетов в день',
                'category': 'other',
                'source_data_type': 'MON',
                'coefficients_codes': ['bracelets_sales_per_day'],
            },
            {
                'name': '21.5 Продажи кулонов в день',
                'code': 'metric_pendants_sales',
                'description': 'Количество проданных кулонов в день',
                'category': 'other',
                'source_data_type': 'MON',
                'coefficients_codes': ['pendants_sales_per_day'],
            },
        ]

        self.stdout.write('\n[3/3] Создание метрик...')
        self.stdout.write('-' * 70)

        for metric_data in metrics_data:
            coefficients_codes = metric_data.pop('coefficients_codes', [])
            formula_code = metric_data.pop('formula_code', None)

            # Получаем формулу если указана
            formula = None
            if formula_code and formula_code in formulas_map:
                formula = formulas_map[formula_code]
                metric_data['formula'] = formula

            metric, created = Metric.objects.get_or_create(
                code=metric_data['code'],
                defaults=metric_data
            )

            # Связываем коэффициенты с метрикой
            for coeff_code in coefficients_codes:
                if coeff_code in coefficients_map:
                    metric.coefficients.add(coefficients_map[coeff_code])

            if created:
                self.stdout.write(self.style.SUCCESS(f'  [+] Создана: {metric.name}'))
            else:
                self.stdout.write(f'  [-] Существует: {metric.name}')

        # ====================================================================
        # ИТОГИ
        # ====================================================================

        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('НАСТРОЙКА ЗАВЕРШЕНА!'))
        self.stdout.write('=' * 70)

        total_coefficients = Coefficient.objects.count()
        total_formulas = Formula.objects.count()
        total_metrics = Metric.objects.count()

        self.stdout.write(f'\nИтоговая статистика:')
        self.stdout.write(f'  - Коэффициентов: {total_coefficients}')
        self.stdout.write(f'  - Формул: {total_formulas}')
        self.stdout.write(f'  - Метрик: {total_metrics}')

        self.stdout.write(f'\n{self.style.SUCCESS("Все 21 метрика настроены и готовы к использованию!")}')
        self.stdout.write(f'\nТеперь вы можете:')
        self.stdout.write(f'  1. Создавать визиты (Visit) в торговые точки')
        self.stdout.write(f'  2. Фиксировать наблюдения (Observation) с замерами коэффициентов')
        self.stdout.write(f'  3. Анализировать метрики в dashboard')
