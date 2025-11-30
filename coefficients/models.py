from django.db import models
from core.constants import DATA_SOURCE_CHOICES, FORMULA_SOURCE_CHOICES


class Coefficient(models.Model):
    """Коэффициент - базовая единица данных для любого типа замера"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    # Типы данных (источник данных)
    data_type = models.CharField(
        'Тип источника данных',
        max_length=10,
        choices=DATA_SOURCE_CHOICES,
        default='MON',
        help_text='Источник данных для коэффициента'
    )

    # Применимость к уровням геоструктуры
    applies_to_outlet = models.BooleanField('Применяется к точке', default=True)
    applies_to_channel = models.BooleanField('Применяется к каналу', default=False)
    applies_to_region = models.BooleanField('Применяется к региону', default=False)
    applies_to_country = models.BooleanField('Применяется к стране', default=False)
    applies_to_global = models.BooleanField('Применяется к глобальному рынку', default=False)

    # Тип данных для коэффициента
    VALUE_TYPE_NUMERIC = 'numeric'
    VALUE_TYPE_TEXT = 'text'
    VALUE_TYPE_BOOLEAN = 'boolean'
    VALUE_TYPE_CHOICES = [
        (VALUE_TYPE_NUMERIC, 'Числовое'),
        (VALUE_TYPE_TEXT, 'Текстовое'),
        (VALUE_TYPE_BOOLEAN, 'Да/Нет'),
    ]
    value_type = models.CharField('Тип значения', max_length=20, choices=VALUE_TYPE_CHOICES, default=VALUE_TYPE_NUMERIC)

    # Единицы измерения
    unit = models.CharField('Единица измерения', max_length=50, blank=True, help_text='Например: штук, кг, %')

    # Статус
    is_active = models.BooleanField('Активен', default=True)

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Коэффициент'
        verbose_name_plural = 'Коэффициенты'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['data_type']),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Metric(models.Model):
    """Метрика - готовый показатель на основе коэффициентов"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    # Связь с коэффициентами
    coefficients = models.ManyToManyField(
        Coefficient,
        verbose_name='Коэффициенты',
        related_name='metrics',
        blank=True
    )

    # Категория метрики
    CATEGORY_DISTRIBUTION = 'distribution'
    CATEGORY_PRICE = 'price'
    CATEGORY_SHARE = 'share'
    CATEGORY_AVAILABILITY = 'availability'
    CATEGORY_OTHER = 'other'
    CATEGORY_CHOICES = [
        (CATEGORY_DISTRIBUTION, 'Дистрибуция'),
        (CATEGORY_PRICE, 'Цена'),
        (CATEGORY_SHARE, 'Доля рынка'),
        (CATEGORY_AVAILABILITY, 'Наличие'),
        (CATEGORY_OTHER, 'Другое'),
    ]
    category = models.CharField('Категория', max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_OTHER)

    # Тип источника данных для расчета метрики
    source_data_type = models.CharField(
        'Тип источника данных',
        max_length=10,
        choices=FORMULA_SOURCE_CHOICES,
        default='MON',
        help_text='Какой тип данных использовать для расчета метрики: мониторинговые, экспертные, ИИ или смешанные (custom)'
    )

    # Формула расчета (связь через Formula)
    formula = models.ForeignKey(
        'Formula',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Формула расчета',
        related_name='metrics'
    )

    # Статус
    is_active = models.BooleanField('Активна', default=True)

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Метрика'
        verbose_name_plural = 'Метрики'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Formula(models.Model):
    """Формула - правило расчета показателей"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    # Тип источника данных для расчета
    source_data_type = models.CharField(
        'Тип источника данных для расчета',
        max_length=10,
        choices=FORMULA_SOURCE_CHOICES,
        default='MON',
        help_text='Какой тип данных использовать для расчета: мониторинговые, экспертные, ИИ или смешанные (custom)'
    )

    # Формула в виде строки
    expression = models.TextField('Выражение', help_text='Формула расчета, например: (C1 + C2) / C3 * 100')

    # Используемые коэффициенты
    coefficients = models.ManyToManyField(
        Coefficient,
        verbose_name='Коэффициенты',
        related_name='formulas',
        blank=True
    )

    # Тип результата
    RESULT_TYPE_NUMERIC = 'numeric'
    RESULT_TYPE_PERCENTAGE = 'percentage'
    RESULT_TYPE_BOOLEAN = 'boolean'
    RESULT_TYPE_CHOICES = [
        (RESULT_TYPE_NUMERIC, 'Числовое'),
        (RESULT_TYPE_PERCENTAGE, 'Процент'),
        (RESULT_TYPE_BOOLEAN, 'Да/Нет'),
    ]
    result_type = models.CharField('Тип результата', max_length=20, choices=RESULT_TYPE_CHOICES, default=RESULT_TYPE_NUMERIC)

    # Единица измерения результата
    result_unit = models.CharField('Единица измерения', max_length=50, blank=True)

    # Статус
    is_active = models.BooleanField('Активна', default=True)

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Формула'
        verbose_name_plural = 'Формулы'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Rule(models.Model):
    """Правило - правила агрегации и обработки данных"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    # Тип правила
    TYPE_AGGREGATION = 'aggregation'
    TYPE_VALIDATION = 'validation'
    TYPE_TRANSFORMATION = 'transformation'
    TYPE_CHOICES = [
        (TYPE_AGGREGATION, 'Агрегация'),
        (TYPE_VALIDATION, 'Валидация'),
        (TYPE_TRANSFORMATION, 'Трансформация'),
    ]
    rule_type = models.CharField('Тип правила', max_length=50, choices=TYPE_CHOICES, default=TYPE_AGGREGATION)

    # Применимость
    applies_to = models.ManyToManyField(
        Coefficient,
        verbose_name='Применяется к коэффициентам',
        related_name='rules',
        blank=True
    )

    # Метод агрегации (для типа aggregation)
    AGGREGATION_SUM = 'sum'
    AGGREGATION_AVG = 'avg'
    AGGREGATION_MIN = 'min'
    AGGREGATION_MAX = 'max'
    AGGREGATION_COUNT = 'count'
    AGGREGATION_CHOICES = [
        (AGGREGATION_SUM, 'Сумма'),
        (AGGREGATION_AVG, 'Среднее'),
        (AGGREGATION_MIN, 'Минимум'),
        (AGGREGATION_MAX, 'Максимум'),
        (AGGREGATION_COUNT, 'Количество'),
    ]
    aggregation_method = models.CharField(
        'Метод агрегации',
        max_length=20,
        choices=AGGREGATION_CHOICES,
        blank=True,
        null=True
    )

    # Параметры правила в JSON
    parameters = models.JSONField('Параметры', default=dict, blank=True, help_text='Дополнительные параметры правила')

    # Статус
    is_active = models.BooleanField('Активно', default=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Правило'
        verbose_name_plural = 'Правила'
        ordering = ['rule_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_rule_type_display()})"
