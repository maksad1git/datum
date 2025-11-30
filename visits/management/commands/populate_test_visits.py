"""
Management команда для загрузки тестовых данных визитов в проект FONON
"""
import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from geo.models import GlobalMarket, Country, Region, Channel, Outlet
from catalog.models import Brand, Category, Product
from coefficients.models import Coefficient
from visits.models import VisitType, Visit, Observation


User = get_user_model()


class Command(BaseCommand):
    help = 'Генерирует тестовые данные визитов для проекта FONON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--visits-per-channel',
            type=int,
            default=20,
            help='Количество визитов на канал сбыта'
        )
        parser.add_argument(
            '--months',
            type=int,
            default=3,
            help='Количество месяцев для генерации данных'
        )

    def handle(self, *args, **options):
        visits_per_channel = options['visits_per_channel']
        months = options['months']

        self.stdout.write(self.style.SUCCESS('Начинаем генерацию тестовых данных...'))

        # Создаем базовую инфраструктуру
        self.create_base_structure()

        # Создаем типы визитов
        visit_types = self.create_visit_types()

        # Создаем коэффициенты
        coefficients = self.create_coefficients()

        # Получаем пользователя для визитов
        user = self.get_or_create_user()

        # Генерируем визиты для каждого канала
        channels = Channel.objects.all()

        total_visits = 0
        for channel in channels:
            self.stdout.write(f'Генерируем визиты для канала: {channel.name}')

            # Получаем или создаем точки сбыта для канала
            outlets = self.get_or_create_outlets(channel, count=5)

            # Генерируем визиты
            visits_created = self.generate_visits(
                channel=channel,
                outlets=outlets,
                visit_types=visit_types,
                coefficients=coefficients,
                user=user,
                count=visits_per_channel,
                months=months
            )
            total_visits += visits_created

        self.stdout.write(self.style.SUCCESS(
            f'Успешно создано {total_visits} визитов для {channels.count()} каналов'
        ))

    def create_base_structure(self):
        """Создает базовую гео-структуру если её нет"""
        # Глобальный рынок
        global_market, _ = GlobalMarket.objects.get_or_create(
            code='GLOBAL',
            defaults={
                'name': 'Глобальный рынок',
                'currency': 'USD',
                'data_type': GlobalMarket.DATA_MIXED
            }
        )

        # Страна
        country, _ = Country.objects.get_or_create(
            code='UZ',
            defaults={
                'global_market': global_market,
                'name': 'Узбекистан',
                'iso_code': 'UZB',
                'currency': 'UZS'
            }
        )

        # Регионы
        regions_data = [
            ('TASHKENT', 'Ташкент'),
            ('SAMARKAND', 'Самарканд'),
            ('BUKHARA', 'Бухара'),
        ]

        for code, name in regions_data:
            Region.objects.get_or_create(
                country=country,
                code=code,
                defaults={'name': name}
            )

        # Каналы сбыта для каждого региона
        channel_types = [
            ('RETAIL', 'Розничные магазины', Channel.TYPE_RETAIL),
            ('WHOLESALE', 'Оптовые базы', Channel.TYPE_WHOLESALE),
            ('ONLINE', 'Онлайн магазины', Channel.TYPE_ONLINE),
            ('HORECA', 'HoReCa', Channel.TYPE_HORECA),
        ]

        for region in Region.objects.all():
            for code, name, channel_type in channel_types:
                Channel.objects.get_or_create(
                    region=region,
                    code=f'{code}_{region.code}',
                    defaults={
                        'name': f'{name} ({region.name})',
                        'type': channel_type
                    }
                )

        self.stdout.write(self.style.SUCCESS('Базовая структура создана'))

    def create_visit_types(self):
        """Создает типы визитов"""
        visit_types_data = [
            {
                'code': 'MONITORING',
                'name': 'Мониторинг цен и наличия',
                'type': VisitType.TYPE_MONITORING,
                'requires_photo': True,
                'requires_gps': True,
            },
            {
                'code': 'AUDIT',
                'name': 'Полный аудит точки',
                'type': VisitType.TYPE_AUDIT,
                'requires_photo': True,
                'requires_signature': True,
                'requires_gps': True,
            },
            {
                'code': 'SURVEY',
                'name': 'Опрос потребителей',
                'type': VisitType.TYPE_SURVEY,
                'requires_signature': True,
            },
            {
                'code': 'INSPECTION',
                'name': 'Проверка выкладки',
                'type': VisitType.TYPE_INSPECTION,
                'requires_photo': True,
            },
        ]

        visit_types = []
        for data in visit_types_data:
            vt, created = VisitType.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            visit_types.append(vt)
            if created:
                self.stdout.write(f'  Создан тип визита: {vt.name}')

        return visit_types

    def create_coefficients(self):
        """Создает коэффициенты для наблюдений"""
        coefficients_data = [
            {
                'code': 'PRICE',
                'name': 'Цена товара',
                'value_type': Coefficient.VALUE_TYPE_NUMERIC,
                'unit': 'сум',
                'data_type': Coefficient.DATA_MONITORING,
            },
            {
                'code': 'STOCK',
                'name': 'Остаток на полке',
                'value_type': Coefficient.VALUE_TYPE_NUMERIC,
                'unit': 'шт',
                'data_type': Coefficient.DATA_MONITORING,
            },
            {
                'code': 'AVAILABILITY',
                'name': 'Наличие товара',
                'value_type': Coefficient.VALUE_TYPE_BOOLEAN,
                'unit': '',
                'data_type': Coefficient.DATA_MONITORING,
            },
            {
                'code': 'SHELF_SHARE',
                'name': 'Доля полки',
                'value_type': Coefficient.VALUE_TYPE_NUMERIC,
                'unit': '%',
                'data_type': Coefficient.DATA_EXPERT,
            },
            {
                'code': 'PROMO',
                'name': 'Промо активность',
                'value_type': Coefficient.VALUE_TYPE_BOOLEAN,
                'unit': '',
                'data_type': Coefficient.DATA_MONITORING,
            },
            {
                'code': 'FACING',
                'name': 'Количество фейсингов',
                'value_type': Coefficient.VALUE_TYPE_NUMERIC,
                'unit': 'шт',
                'data_type': Coefficient.DATA_MONITORING,
            },
            {
                'code': 'VISIBILITY',
                'name': 'Видимость товара',
                'value_type': Coefficient.VALUE_TYPE_NUMERIC,
                'unit': 'балл (1-10)',
                'data_type': Coefficient.DATA_EXPERT,
            },
        ]

        coefficients = []
        for data in coefficients_data:
            coef, created = Coefficient.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            coefficients.append(coef)
            if created:
                self.stdout.write(f'  Создан коэффициент: {coef.name}')

        return coefficients

    def get_or_create_user(self):
        """Получает или создает пользователя для визитов"""
        user = User.objects.filter(is_staff=True).first()
        if not user:
            user = User.objects.create_user(
                username='merchandiser1',
                email='merchandiser@example.com',
                password='test123',
                first_name='Иван',
                last_name='Иванов'
            )
            self.stdout.write('  Создан пользователь: merchandiser1')
        return user

    def get_or_create_outlets(self, channel, count=5):
        """Получает или создает точки сбыта для канала"""
        existing_outlets = list(channel.outlets.all())

        if len(existing_outlets) >= count:
            return existing_outlets[:count]

        outlets = list(existing_outlets)

        # Создаем недостающие точки
        outlet_names = [
            'Магазин №1', 'Магазин №2', 'Магазин №3',
            'Супермаркет Центральный', 'Магазин у дома',
            'Торговый центр', 'Минимаркет', 'Гипермаркет',
        ]

        for i in range(len(existing_outlets), count):
            outlet = Outlet.objects.create(
                channel=channel,
                name=f'{outlet_names[i % len(outlet_names)]} - {channel.name}',
                code=f'OUT_{channel.code}_{i+1}',
                address=f'ул. Тестовая, {i+1}',
                contact_phone=f'+998901234{i:04d}',
                latitude=Decimal(str(41.3 + random.uniform(-0.1, 0.1))),
                longitude=Decimal(str(69.3 + random.uniform(-0.1, 0.1))),
                status=Outlet.STATUS_ACTIVE
            )
            outlets.append(outlet)

        return outlets

    def get_or_create_products(self, count=10):
        """Получает или создает товары"""
        existing_products = list(Product.objects.all()[:count])

        if len(existing_products) >= count:
            return existing_products

        # Создаем бренд и категорию если нужно
        brand, _ = Brand.objects.get_or_create(
            code='TEST_BRAND',
            defaults={'name': 'Тестовый бренд'}
        )

        category, _ = Category.objects.get_or_create(
            code='TEST_CAT',
            defaults={'name': 'Тестовая категория'}
        )

        products = list(existing_products)

        product_names = [
            'Молоко 1л', 'Хлеб белый', 'Яйца 10шт', 'Сахар 1кг',
            'Масло подсолнечное 1л', 'Рис 1кг', 'Мука 1кг', 'Соль 1кг',
            'Чай черный 100г', 'Кофе растворимый 100г', 'Макароны 500г',
            'Печенье 200г', 'Шоколад 100г', 'Вода 1.5л', 'Сок 1л'
        ]

        for i in range(len(existing_products), count):
            product = Product.objects.create(
                brand=brand,
                category=category,
                name=product_names[i % len(product_names)],
                sku_code=f'SKU_{i+1:04d}',
                price=Decimal(str(random.uniform(5000, 50000))),
                status=Product.STATUS_ACTIVE
            )
            products.append(product)

        return products

    def generate_visits(self, channel, outlets, visit_types, coefficients, user, count, months):
        """Генерирует визиты для канала"""
        visits_created = 0

        # Получаем товары
        products = self.get_or_create_products(count=10)

        # Генерируем даты визитов за указанный период
        end_date = timezone.now()
        start_date = end_date - timedelta(days=months * 30)

        for i in range(count):
            # Случайная дата в пределах периода
            random_days = random.randint(0, months * 30)
            visit_date = start_date + timedelta(days=random_days)

            # Случайный тип визита
            visit_type = random.choice(visit_types)

            # Случайная точка сбыта
            outlet = random.choice(outlets)

            # Определяем статус визита (больше завершенных, меньше планируемых)
            status = random.choices(
                [Visit.STATUS_COMPLETED, Visit.STATUS_PLANNED, Visit.STATUS_CANCELLED],
                weights=[80, 15, 5],
                k=1
            )[0]

            # Создаем визит
            visit = Visit.objects.create(
                visit_type=visit_type,
                outlet=outlet,
                user=user,
                planned_date=visit_date,
                start_date=visit_date if status != Visit.STATUS_PLANNED else None,
                end_date=visit_date + timedelta(hours=random.randint(1, 3)) if status == Visit.STATUS_COMPLETED else None,
                status=status,
                latitude=outlet.latitude + Decimal(str(random.uniform(-0.001, 0.001))) if outlet.latitude else None,
                longitude=outlet.longitude + Decimal(str(random.uniform(-0.001, 0.001))) if outlet.longitude else None,
                notes=self.generate_random_notes(status),
                form_data=self.generate_form_data(visit_type)
            )

            # Создаем наблюдения только для завершенных визитов
            if status == Visit.STATUS_COMPLETED:
                self.create_observations(visit, coefficients, products)

            visits_created += 1

        return visits_created

    def create_observations(self, visit, coefficients, products):
        """Создает наблюдения для визита"""
        # Количество наблюдений варьируется
        num_observations = random.randint(3, 8)

        # Выбираем случайные коэффициенты
        selected_coefficients = random.sample(coefficients, min(num_observations, len(coefficients)))

        for coefficient in selected_coefficients:
            # Для некоторых коэффициентов привязываем товар
            product = None
            if coefficient.code in ['PRICE', 'STOCK', 'AVAILABILITY', 'FACING']:
                product = random.choice(products)

            # Генерируем значение в зависимости от типа коэффициента
            if coefficient.value_type == Coefficient.VALUE_TYPE_NUMERIC:
                if coefficient.code == 'PRICE':
                    value_numeric = Decimal(str(random.uniform(5000, 80000)))
                elif coefficient.code == 'STOCK':
                    value_numeric = Decimal(str(random.randint(0, 50)))
                elif coefficient.code == 'SHELF_SHARE':
                    value_numeric = Decimal(str(random.uniform(5, 40)))
                elif coefficient.code == 'FACING':
                    value_numeric = Decimal(str(random.randint(1, 10)))
                elif coefficient.code == 'VISIBILITY':
                    value_numeric = Decimal(str(random.randint(1, 10)))
                else:
                    value_numeric = Decimal(str(random.uniform(0, 100)))

                Observation.objects.create(
                    visit=visit,
                    coefficient=coefficient,
                    product=product,
                    value_numeric=value_numeric,
                    notes=self.generate_observation_notes()
                )

            elif coefficient.value_type == Coefficient.VALUE_TYPE_BOOLEAN:
                Observation.objects.create(
                    visit=visit,
                    coefficient=coefficient,
                    product=product,
                    value_boolean=random.choice([True, False]),
                    notes=self.generate_observation_notes()
                )

    def generate_random_notes(self, status):
        """Генерирует случайные комментарии для визита"""
        if status == Visit.STATUS_COMPLETED:
            notes = [
                'Визит прошел успешно, все данные собраны',
                'Отличное сотрудничество с менеджером точки',
                'Найдены интересные инсайты по конкурентам',
                'Проблемы с выкладкой, обсудили с администратором',
                'Все товары в наличии, цены стабильные',
            ]
        elif status == Visit.STATUS_PLANNED:
            notes = [
                'Визит запланирован',
                'Согласовано время визита с менеджером',
                'Подготовлены материалы для визита',
            ]
        else:
            notes = [
                'Визит отменен по причине болезни',
                'Точка была закрыта на ремонт',
                'Перенесено по просьбе клиента',
            ]

        return random.choice(notes)

    def generate_observation_notes(self):
        """Генерирует случайные комментарии для наблюдения"""
        notes = [
            '',
            'Товар на акции',
            'Близко к истечению срока годности',
            'Новое поступление',
            'Требуется пополнение',
            'Хорошая видимость',
            'Плохая выкладка',
        ]
        return random.choice(notes)

    def generate_form_data(self, visit_type):
        """Генерирует случайные данные формы"""
        form_data = {
            'store_cleanliness': random.randint(1, 10),
            'staff_friendliness': random.randint(1, 10),
            'has_parking': random.choice([True, False]),
        }

        if visit_type.code == 'AUDIT':
            form_data.update({
                'refrigeration_working': random.choice([True, False]),
                'pos_materials_present': random.choice([True, False]),
                'competitor_presence': random.choice([True, False]),
            })

        if visit_type.code == 'SURVEY':
            form_data.update({
                'customers_surveyed': random.randint(5, 20),
                'satisfaction_score': random.uniform(3.0, 5.0),
            })

        return form_data
