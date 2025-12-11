from django.core.management.base import BaseCommand
from geo.models import Country, Region, City, District


class Command(BaseCommand):
    help = 'Load Uzbekistan geographic data'

    def handle(self, *args, **options):
        self.stdout.write('Loading Uzbekistan geographic data...')

        # Create or get Uzbekistan country
        country, created = Country.objects.get_or_create(
            code='UZ',
            defaults={
                'name': 'Узбекистан',
                'data_type': 'actual'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created country: {country.name}'))
        else:
            self.stdout.write(f'Country already exists: {country.name}')

        # Data structure: region_name: {cities: {city_name: [districts]}}
        uzbekistan_data = {
            'Республика Каракалпакстан': {
                'Нукус': ['Центральный', 'Южный', 'Северный', 'Восточный'],
                'Ходжейли': [],
                'Шуманай': [],
                'Кунград': [],
                'Муйнак': [],
                'Чимбай': [],
                'Тахиаташ': [],
                'Турткуль': [],
                'Караузяк': [],
                'Канлыкуль': [],
                'Кегейли': [],
            },
            'Андижанская область': {
                'Андижан': ['Бобур', 'Асака', 'Шахрихон', 'Тайлак', 'Корасув'],
                'Асака': [],
                'Шахрихан': [],
            },
            'Бухарская область': {
                'Бухара': ['Центральный', 'Северный', 'Южный', 'Восточный'],
                'Каган': ['Центральный'],
                'Газли': [],
                'Каракуль': [],
                'Вабкент': [],
                'Галаасия': [],
                'Когон': [],
                'Гиждуван': [],
                'Шафиркан': [],
            },
            'Джизакская область': {
                'Джизак': ['Центральный', 'Паст-Даргом', 'Зарбдор'],
                'Дустлик': [],
                'Пахтакор': [],
            },
            'Кашкадарьинская область': {
                'Карши': ['Центральный', 'Туманский', 'Китабский'],
                'Шахрисабз': [],
                'Китаб': [],
                'Мубарак': [],
                'Гузар': [],
            },
            'Навоийская область': {
                'Навои': ['Центральный', 'Западный', 'Восточный', 'Кызылтепинский'],
                'Зарафшан': [],
                'Учкудук': [],
            },
            'Наманганская область': {
                'Наманган': ['Центральный', 'Сохибкор', 'Косонсой', 'Янгиша'],
                'Чартак': [],
                'Учкурган': [],
                'Уйчи': [],
                'Чуст': [],
                'Янгикурган': [],
                'Туракурган': [],
            },
            'Самаркандская область': {
                'Самарканд': ['Центральный', 'Северный', 'Южный', 'Восточный'],
                'Каттакурган': [],
                'Каган': [],
                'Жомбой': [],
                'Ургут': [],
                'Пайарык': [],
                'Нурабад': [],
            },
            'Сурхандарьинская область': {
                'Термез': ['Центральный', 'Северный', 'Южный'],
                'Денов': [],
                'Шеробод': [],
                'Ангор': [],
                'Байсун': [],
            },
            'Сырдарьинская область': {
                'Гулистан': ['Центральный', 'Мирзаабад', 'Ширин'],
                'Янгиер': [],
                'Сырдарья': [],
            },
            'Ташкентская область': {
                'Алмалык': [],
                'Ангрен': [],
                'Бекабад': [],
                'Чирчик': [],
                'Нурафшон': [],
                'Газалкент': [],
                'Янгиюль': [],
                'Паркент': [],
                'Ахангаран': [],
                'Келес': [],
            },
            'Ферганская область': {
                'Фергана': ['Центральный', 'Северный', 'Южный', 'Западный'],
                'Коканд': ['Центральный', 'Северный'],
                'Маргилан': [],
                'Кува': [],
                'Риштан': [],
                'Шахимардан': [],
            },
            'Хорезмская область': {
                'Ургенч': ['Центральный', 'Северный', 'Южный'],
                'Хива': [],
                'Питнак': [],
                'Янгиарык': [],
                'Ханка': [],
            },
            'Город Ташкент': {
                'Ташкент': [
                    'Алмазарский', 'Бектемирский', 'Мирабадский', 'Миробадский',
                    'Сергелийский', 'Шайхонтохурский', 'Учтепинский', 'Юнусабадский',
                    'Яшнободский', 'Яккасарайский', 'Чиланзарский'
                ],
            },
        }

        regions_created = 0
        cities_created = 0
        districts_created = 0

        for region_name, cities_data in uzbekistan_data.items():
            # Create region
            region, created = Region.objects.get_or_create(
                country=country,
                name=region_name,
                defaults={
                    'code': self._generate_code(region_name),
                    'data_type': 'actual'
                }
            )
            if created:
                regions_created += 1
                self.stdout.write(f'  Created region: {region_name}')

            for city_name, districts_list in cities_data.items():
                # Create city
                city, created = City.objects.get_or_create(
                    region=region,
                    name=city_name,
                    defaults={
                        'code': self._generate_code(city_name),
                        'data_type': 'actual'
                    }
                )
                if created:
                    cities_created += 1
                    self.stdout.write(f'    Created city: {city_name}')

                # Create districts
                for district_name in districts_list:
                    district, created = District.objects.get_or_create(
                        city=city,
                        name=district_name,
                        defaults={
                            'code': self._generate_code(district_name),
                            'data_type': 'actual'
                        }
                    )
                    if created:
                        districts_created += 1
                        self.stdout.write(f'      Created district: {district_name}')

        self.stdout.write(self.style.SUCCESS(f'\nSummary:'))
        self.stdout.write(self.style.SUCCESS(f'  Regions created: {regions_created}'))
        self.stdout.write(self.style.SUCCESS(f'  Cities created: {cities_created}'))
        self.stdout.write(self.style.SUCCESS(f'  Districts created: {districts_created}'))
        self.stdout.write(self.style.SUCCESS('\nUzbekistan data loaded successfully!'))

    def _generate_code(self, name):
        """Generate a simple code from name"""
        # Remove spaces and special characters, take first 10 chars
        import re
        code = re.sub(r'[^a-zA-Z0-9а-яА-Я]', '', name)
        return code[:10].upper()
