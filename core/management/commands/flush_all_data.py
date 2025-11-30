"""
Management command для полной очистки всех данных из базы данных.
Удаляет все записи из всех таблиц, оставляя только структуру БД.
"""
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection


class Command(BaseCommand):
    help = 'Полностью очистить все данные из базы данных (кроме миграций)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--yes',
            action='store_true',
            help='Подтвердить удаление без запроса',
        )

    def handle(self, *args, **options):
        if not options['yes']:
            confirm = input(
                '\n'
                '[!] ВНИМАНИЕ! Эта команда удалит ВСЕ данные из базы данных!\n'
                '    - Все страны, регионы, каналы, магазины\n'
                '    - Все продукты, категории, бренды\n'
                '    - Все визиты и наблюдения\n'
                '    - Все коэффициенты и метрики\n'
                '    - Все пользователи (кроме суперпользователя)\n'
                '    - Все формы и шаблоны отчетов\n'
                '\n'
                'Вы уверены? Введите "yes" для продолжения: '
            )
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Операция отменена'))
                return

        self.stdout.write(self.style.WARNING('\n[!] Начинаем очистку базы данных...\n'))

        # Получить все модели
        all_models = apps.get_models()

        # Исключить системные модели Django
        exclude_models = [
            'ContentType',
            'Permission',
            'Session',
            'LogEntry',
            'Migration',
        ]

        deleted_counts = {}
        total_deleted = 0

        # Отключить проверку внешних ключей
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = OFF;')

        try:
            for model in all_models:
                model_name = model.__name__

                # Пропустить системные модели
                if model_name in exclude_models:
                    continue

                # Получить количество записей
                count = model.objects.count()

                if count > 0:
                    # Специальная обработка для User - не удалять суперпользователей
                    if model_name == 'User':
                        # Удалить только обычных пользователей
                        deleted = model.objects.filter(is_superuser=False).delete()
                        deleted_count = deleted[0] if deleted else 0

                        if deleted_count > 0:
                            deleted_counts[f'{model._meta.app_label}.{model_name}'] = deleted_count
                            total_deleted += deleted_count
                            self.stdout.write(
                                self.style.SUCCESS(f'  [+] {model._meta.app_label}.{model_name}: удалено {deleted_count} записей (суперпользователи сохранены)')
                            )

                        # Показать сколько суперпользователей осталось
                        superusers_count = model.objects.filter(is_superuser=True).count()
                        if superusers_count > 0:
                            self.stdout.write(
                                self.style.WARNING(f'  [*] Сохранено суперпользователей: {superusers_count}')
                            )
                    else:
                        # Удалить все записи для других моделей
                        model.objects.all().delete()
                        deleted_counts[f'{model._meta.app_label}.{model_name}'] = count
                        total_deleted += count

                        self.stdout.write(
                            self.style.SUCCESS(f'  [+] {model._meta.app_label}.{model_name}: удалено {count} записей')
                        )

        finally:
            # Включить проверку внешних ключей обратно
            with connection.cursor() as cursor:
                cursor.execute('PRAGMA foreign_keys = ON;')

        # Вывести итоги
        self.stdout.write(
            self.style.SUCCESS(
                f'\n[OK] Готово! Удалено записей: {total_deleted}\n'
                f'     Затронуто моделей: {len(deleted_counts)}\n'
            )
        )

        # Вывести детальную статистику
        if deleted_counts:
            self.stdout.write('\n[STAT] Детальная статистика:')
            for model_path, count in sorted(deleted_counts.items()):
                self.stdout.write(f'       - {model_path}: {count}')

        self.stdout.write(
            self.style.WARNING(
                '\n[!] База данных полностью очищена!\n'
                '    Структура таблиц сохранена.\n'
                '    Можно начинать заполнение данных заново.\n'
            )
        )
