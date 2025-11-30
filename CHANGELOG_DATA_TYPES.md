# Changelog: Добавление source_data_type для метрик

## Дата: 2025-11-30

## Изменения

### 1. Модель Metric (coefficients/models.py)

**Добавлено новое поле:**
```python
source_data_type = models.CharField(
    'Тип источника данных',
    max_length=10,
    choices=FORMULA_SOURCE_CHOICES,
    default='MON',
    help_text='Какой тип данных использовать для расчета метрики'
)
```

**Причина:** Метрики теперь могут явно указывать, какой тип данных использовать для расчета:
- MON - только мониторинговые данные
- EXP - только экспертные данные
- AI - только данные из ИИ анализа
- CUSTOM - смешанные данные (комбинация типов)

### 2. Форма MetricForm (coefficients/forms.py)

**Добавлен виджет:**
```python
'source_data_type': forms.Select(attrs={
    'class': 'form-select'
}),
```

### 3. Форма FormulaForm (coefficients/forms.py)

**Добавлен виджет:**
```python
'source_data_type': forms.Select(attrs={
    'class': 'form-select'
}),
```

### 4. Шаблон metric_detail.html

**Добавлено отображение типа источника данных:**
```html
<dt class="col-sm-5">Тип источника данных:</dt>
<dd class="col-sm-7">
    {% if object.source_data_type == 'MON' %}
    <span class="badge bg-primary">...</span>
    {% elif object.source_data_type == 'EXP' %}
    <span class="badge bg-success">...</span>
    ...
    {% endif %}
</dd>
```

### 5. Миграция базы данных

**Создана и применена миграция:**
- `coefficients/migrations/0003_metric_source_data_type.py`

## Проверка изменений

Создан скрипт проверки `check_data_types.py`, который подтверждает:

✅ Coefficient.data_type - существует
✅ Formula.source_data_type - существует
✅ Metric.source_data_type - существует (НОВОЕ!)
✅ Visit.data_source_type - существует
✅ Observation.data_source_type - существует
✅ AttributeDefinition.data_source_type - корректно отсутствует
✅ ProductAttributeValue.data_source_type - корректно отсутствует

## Документация

Создана документация `DATA_SOURCE_TYPES.md`, описывающая полную систему типов источников данных в DATUM.

## Совместимость

- **Обратная совместимость:** ДА
- **Требуется миграция:** ДА (уже применена)
- **Влияние на существующие данные:** Минимальное (новое поле имеет default='MON')

## Использование

### Пример 1: Метрика только для мониторинговых данных
```python
metric = Metric.objects.create(
    name='Средняя цена (мониторинг)',
    code='avg_price_mon',
    source_data_type='MON',
    ...
)
```

### Пример 2: Метрика только для экспертных данных
```python
metric = Metric.objects.create(
    name='Средняя цена (эксперт)',
    code='avg_price_exp',
    source_data_type='EXP',
    ...
)
```

### Пример 3: Метрика для данных ИИ
```python
metric = Metric.objects.create(
    name='Анализ цен ИИ',
    code='ai_price_analysis',
    source_data_type='AI',
    ...
)
```

### Пример 4: Метрика со смешанными данными
```python
metric = Metric.objects.create(
    name='Общая дистрибуция',
    code='overall_distribution',
    source_data_type='CUSTOM',
    ...
)
```

## Архитектурные решения

1. **Независимость от формулы:** Метрика имеет собственное поле source_data_type, независимое от связанной формулы. Это дает гибкость в настройке.

2. **Согласованность с Formula:** Используется тот же набор choices (FORMULA_SOURCE_CHOICES), что и у Formula.source_data_type.

3. **Значение по умолчанию:** По умолчанию используется 'MON' (мониторинг), как наиболее распространенный тип данных.

## Связанные файлы

- `coefficients/models.py` - модель Metric
- `coefficients/forms.py` - формы MetricForm и FormulaForm
- `templates/coefficients/metric_detail.html` - шаблон детального просмотра
- `coefficients/migrations/0003_metric_source_data_type.py` - миграция
- `DATA_SOURCE_TYPES.md` - документация по системе типов данных
- `check_data_types.py` - скрипт проверки корректности полей
