"""
Скрипт для добавления Dashboard записей для City и District уровней
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datum_project.settings')
django.setup()

from analytics.models import Dashboard
from django.contrib.auth import get_user_model

User = get_user_model()

# Получить первого админа или superuser
admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()

if not admin_user:
    print("❌ Нет пользователей в системе! Создайте пользователя сначала.")
    exit(1)

print(f"Использую владельца: {admin_user.username}")

# Проверка существующих дашбордов
existing = Dashboard.objects.filter(level__in=['city', 'district'])
print(f"Найдено существующих дашбордов для city/district: {existing.count()}")

if existing.count() > 0:
    print("Удаляю существующие записи...")
    existing.delete()

# Создание Dashboard для City
city_dashboard = Dashboard.objects.create(
    name="Дашборд по городам",
    code="city_dashboard",
    owner=admin_user,
    dashboard_type='overview',
    level='city',
    level_icon='🏙️',
    level_order=3,
    description="Анализ данных на уровне городов",
    widgets_config=[],
    is_public=True,
    is_active=True
)
print(f"✅ Создан дашборд для City: {city_dashboard.name}")

# Создание Dashboard для District
district_dashboard = Dashboard.objects.create(
    name="Дашборд по районам",
    code="district_dashboard",
    owner=admin_user,
    dashboard_type='overview',
    level='district',
    level_icon='🏘️',
    level_order=4,
    description="Анализ данных на уровне районов",
    widgets_config=[],
    is_public=True,
    is_active=True
)
print(f"✅ Создан дашборд для District: {district_dashboard.name}")

# Проверка
all_dashboards = Dashboard.objects.filter(level__isnull=False).order_by('level_order')
print(f"\nВсе мультиуровневые дашборды ({all_dashboards.count()}):")
for dash in all_dashboards:
    print(f"  {dash.level_order}. {dash.level_icon} {dash.level} - {dash.name}")

print("\n✅ Готово!")
