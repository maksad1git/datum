"""
Скрипт для проверки полей data_type/source_data_type в моделях DATUM
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datum_project.settings')
django.setup()

from coefficients.models import Coefficient, Metric, Formula
from visits.models import Visit, Observation
from catalog.models import AttributeDefinition, ProductAttributeValue

def check_model_field(model, field_name):
    """Проверяет наличие поля в модели"""
    try:
        field = model._meta.get_field(field_name)
        return True, f"[OK] {model.__name__}.{field_name} exists"
    except Exception as e:
        return False, f"[FAIL] {model.__name__}.{field_name} NOT FOUND"

print("=" * 70)
print("CHECK DATA_TYPE/SOURCE_DATA_TYPE FIELDS IN DATUM MODELS")
print("=" * 70)

print("\n[SHOULD HAVE data_type/source_data_type]")
print("-" * 70)

# Модели, которые ДОЛЖНЫ иметь поля
has_field = [
    (Coefficient, 'data_type'),
    (Formula, 'source_data_type'),
    (Metric, 'source_data_type'),
    (Visit, 'data_source_type'),
    (Observation, 'data_source_type'),
]

all_passed = True
for model, field in has_field:
    result, message = check_model_field(model, field)
    print(message)
    if not result:
        all_passed = False

print("\n[SHOULD NOT HAVE data_type/source_data_type]")
print("-" * 70)

# Модели, которые НЕ ДОЛЖНЫ иметь поля
should_not_have = [
    (AttributeDefinition, 'data_source_type'),
    (ProductAttributeValue, 'data_source_type'),
]

for model, field in should_not_have:
    result, message = check_model_field(model, field)
    if result:
        print(f"[FAIL] {model.__name__}.{field} exists, but SHOULD NOT!")
        all_passed = False
    else:
        print(f"[OK] {model.__name__}.{field} correctly absent")

print("\n" + "=" * 70)
if all_passed:
    print("[SUCCESS] ALL CHECKS PASSED!")
else:
    print("[ERROR] SOME CHECKS FAILED!")
print("=" * 70)

# Дополнительная информация
print("\n[FIELD INFORMATION]")
print("-" * 70)

print("\nCoefficient.data_type:")
field = Coefficient._meta.get_field('data_type')
print(f"  Type: {field.get_internal_type()}")
print(f"  Choices: {field.choices}")

print("\nMetric.source_data_type:")
field = Metric._meta.get_field('source_data_type')
print(f"  Type: {field.get_internal_type()}")
print(f"  Choices: {field.choices}")

print("\nFormula.source_data_type:")
field = Formula._meta.get_field('source_data_type')
print(f"  Type: {field.get_internal_type()}")
print(f"  Choices: {field.choices}")

print("\nObservation.data_source_type:")
field = Observation._meta.get_field('data_source_type')
print(f"  Type: {field.get_internal_type()}")
print(f"  Choices: {field.choices}")

print("\nVisit.data_source_type:")
field = Visit._meta.get_field('data_source_type')
print(f"  Type: {field.get_internal_type()}")
print(f"  Choices: {field.choices}")
