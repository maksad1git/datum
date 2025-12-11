from django.db import models
from django.conf import settings


class Dashboard(models.Model):
    """Дашборд - настройка панели аналитики"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    # Владелец дашборда
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='dashboards'
    )

    # Тип дашборда
    TYPE_OVERVIEW = 'overview'
    TYPE_DISTRIBUTION = 'distribution'
    TYPE_SALES = 'sales'
    TYPE_CUSTOM = 'custom'
    TYPE_CHOICES = [
        (TYPE_OVERVIEW, 'Обзорный'),
        (TYPE_DISTRIBUTION, 'Дистрибуция'),
        (TYPE_SALES, 'Продажи'),
        (TYPE_CUSTOM, 'Пользовательский'),
    ]
    dashboard_type = models.CharField('Тип', max_length=50, choices=TYPE_CHOICES, default=TYPE_OVERVIEW)

    # Уровень иерархии (для мультиуровневых дашбордов)
    LEVEL_COUNTRY = 'country'
    LEVEL_REGION = 'region'
    LEVEL_CITY = 'city'
    LEVEL_DISTRICT = 'district'
    LEVEL_CHANNEL = 'channel'
    LEVEL_OUTLET = 'outlet'
    LEVEL_CHOICES = [
        (LEVEL_COUNTRY, 'Страна'),
        (LEVEL_REGION, 'Регион'),
        (LEVEL_CITY, 'Город'),
        (LEVEL_DISTRICT, 'Район'),
        (LEVEL_CHANNEL, 'Канал сбыта'),
        (LEVEL_OUTLET, 'Торговая точка'),
    ]
    level = models.CharField('Уровень иерархии', max_length=50, choices=LEVEL_CHOICES, blank=True, null=True)
    level_icon = models.CharField('Иконка уровня', max_length=10, blank=True, help_text='Эмодзи для отображения в переключателе')
    level_order = models.PositiveIntegerField('Порядок уровня', default=0, help_text='Порядок отображения в переключателе')

    # Конфигурация виджетов в JSON
    # Пример: [
    #   {
    #     "widget_type": "chart",
    #     "chart_type": "line",
    #     "title": "Динамика визитов",
    #     "data_source": "visits",
    #     "filters": {...},
    #     "position": {"x": 0, "y": 0, "w": 6, "h": 4}
    #   }
    # ]
    widgets_config = models.JSONField('Конфигурация виджетов', default=list, blank=True)

    # Фильтры по умолчанию
    default_filters = models.JSONField('Фильтры по умолчанию', default=dict, blank=True)

    # Период обновления (в минутах)
    refresh_interval = models.PositiveIntegerField('Интервал обновления (мин)', default=15)

    # Публичный доступ
    is_public = models.BooleanField('Публичный', default=False)
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name='Доступен пользователям',
        related_name='shared_dashboards',
        blank=True
    )

    # Статус
    is_active = models.BooleanField('Активен', default=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Дашборд'
        verbose_name_plural = 'Дашборды'
        ordering = ['name']
        indexes = [
            models.Index(fields=['owner', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.owner.get_full_name() or self.owner.username})"


class Report(models.Model):
    """Отчет - сгенерированный отчет"""
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)

    # Шаблон отчета
    template = models.ForeignKey(
        'ReportTemplate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Шаблон',
        related_name='reports'
    )

    # Создатель
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Создал',
        related_name='reports'
    )

    # Период отчета
    date_from = models.DateField('Дата с', null=True, blank=True)
    date_to = models.DateField('Дата по', null=True, blank=True)

    # Фильтры отчета
    filters = models.JSONField('Фильтры', default=dict, blank=True)

    # Данные отчета (кэш результатов)
    data = models.JSONField('Данные', default=dict, blank=True)

    # Формат отчета
    FORMAT_HTML = 'html'
    FORMAT_PDF = 'pdf'
    FORMAT_EXCEL = 'excel'
    FORMAT_CSV = 'csv'
    FORMAT_CHOICES = [
        (FORMAT_HTML, 'HTML'),
        (FORMAT_PDF, 'PDF'),
        (FORMAT_EXCEL, 'Excel'),
        (FORMAT_CSV, 'CSV'),
    ]
    format = models.CharField('Формат', max_length=20, choices=FORMAT_CHOICES, default=FORMAT_HTML)

    # Файл отчета (если сохранен)
    file = models.FileField('Файл', upload_to='reports/%Y/%m/', blank=True, null=True)

    # Статус генерации
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидание'),
        (STATUS_PROCESSING, 'Обработка'),
        (STATUS_COMPLETED, 'Завершен'),
        (STATUS_FAILED, 'Ошибка'),
    ]
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # Время генерации
    generated_at = models.DateTimeField('Дата генерации', null=True, blank=True)
    generation_time = models.FloatField('Время генерации (сек)', null=True, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"


class ReportTemplate(models.Model):
    """Шаблон отчета"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    # Тип отчета
    TYPE_SUMMARY = 'summary'
    TYPE_DETAILED = 'detailed'
    TYPE_COMPARISON = 'comparison'
    TYPE_TREND = 'trend'
    TYPE_CUSTOM = 'custom'
    TYPE_CHOICES = [
        (TYPE_SUMMARY, 'Сводный'),
        (TYPE_DETAILED, 'Детальный'),
        (TYPE_COMPARISON, 'Сравнительный'),
        (TYPE_TREND, 'Трендовый'),
        (TYPE_CUSTOM, 'Пользовательский'),
    ]
    report_type = models.CharField('Тип отчета', max_length=50, choices=TYPE_CHOICES, default=TYPE_SUMMARY)

    # Категория
    CATEGORY_DISTRIBUTION = 'distribution'
    CATEGORY_SALES = 'sales'
    CATEGORY_VISITS = 'visits'
    CATEGORY_PRODUCTS = 'products'
    CATEGORY_OTHER = 'other'
    CATEGORY_CHOICES = [
        (CATEGORY_DISTRIBUTION, 'Дистрибуция'),
        (CATEGORY_SALES, 'Продажи'),
        (CATEGORY_VISITS, 'Визиты'),
        (CATEGORY_PRODUCTS, 'Товары'),
        (CATEGORY_OTHER, 'Другое'),
    ]
    category = models.CharField('Категория', max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_OTHER)

    # Конфигурация отчета
    config = models.JSONField('Конфигурация', default=dict, blank=True, help_text='Структура и параметры отчета')

    # SQL запрос (для сложных отчетов)
    sql_query = models.TextField('SQL запрос', blank=True)

    # Метрики для отчета
    metrics = models.ManyToManyField(
        'coefficients.Metric',
        verbose_name='Метрики',
        related_name='report_templates',
        blank=True
    )

    # Создатель
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создал',
        related_name='report_templates'
    )

    # Статус
    is_active = models.BooleanField('Активен', default=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Шаблон отчета'
        verbose_name_plural = 'Шаблоны отчетов'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class FilterPreset(models.Model):
    """Набор фильтров - сохраненные настройки фильтрации"""
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)

    # Владелец
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='filter_presets'
    )

    # Тип фильтра (к чему применяется)
    APPLIES_TO_DASHBOARD = 'dashboard'
    APPLIES_TO_REPORT = 'report'
    APPLIES_TO_VISIT = 'visit'
    APPLIES_TO_PRODUCT = 'product'
    APPLIES_TO_CHOICES = [
        (APPLIES_TO_DASHBOARD, 'Дашборд'),
        (APPLIES_TO_REPORT, 'Отчет'),
        (APPLIES_TO_VISIT, 'Визит'),
        (APPLIES_TO_PRODUCT, 'Товар'),
    ]
    applies_to = models.CharField('Применяется к', max_length=50, choices=APPLIES_TO_CHOICES, default=APPLIES_TO_DASHBOARD)

    # Параметры фильтров
    # Пример: {
    #   "date_from": "2024-01-01",
    #   "date_to": "2024-12-31",
    #   "countries": [1, 2, 3],
    #   "channels": [5, 6],
    #   "brands": [10, 11]
    # }
    filters = models.JSONField('Фильтры', default=dict)

    # Публичный доступ
    is_public = models.BooleanField('Публичный', default=False)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Набор фильтров'
        verbose_name_plural = 'Наборы фильтров'
        ordering = ['owner', 'name']

    def __str__(self):
        return f"{self.name} ({self.owner.get_full_name() or self.owner.username})"


class ForecastModel(models.Model):
    """Модель прогнозирования - базовая модель для прогнозов"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    # Тип модели
    MODEL_TYPE_LINEAR = 'linear'
    MODEL_TYPE_EXPONENTIAL = 'exponential'
    MODEL_TYPE_SEASONAL = 'seasonal'
    MODEL_TYPE_ARIMA = 'arima'
    MODEL_TYPE_CUSTOM = 'custom'
    MODEL_TYPE_CHOICES = [
        (MODEL_TYPE_LINEAR, 'Линейная'),
        (MODEL_TYPE_EXPONENTIAL, 'Экспоненциальная'),
        (MODEL_TYPE_SEASONAL, 'Сезонная'),
        (MODEL_TYPE_ARIMA, 'ARIMA'),
        (MODEL_TYPE_CUSTOM, 'Пользовательская'),
    ]
    model_type = models.CharField('Тип модели', max_length=50, choices=MODEL_TYPE_CHOICES, default=MODEL_TYPE_LINEAR)

    # Применяется к метрикам
    metrics = models.ManyToManyField(
        'coefficients.Metric',
        verbose_name='Метрики',
        related_name='forecast_models',
        blank=True
    )

    # Параметры модели
    parameters = models.JSONField('Параметры', default=dict, blank=True)

    # Результаты обучения
    training_data = models.JSONField('Данные обучения', default=dict, blank=True)
    training_score = models.FloatField('Точность модели', null=True, blank=True)

    # Период прогноза (дней)
    forecast_horizon = models.PositiveIntegerField('Горизонт прогноза (дней)', default=30)

    # Создатель
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создал',
        related_name='forecast_models'
    )

    # Статус
    STATUS_DRAFT = 'draft'
    STATUS_TRAINING = 'training'
    STATUS_ACTIVE = 'active'
    STATUS_ARCHIVED = 'archived'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_TRAINING, 'Обучение'),
        (STATUS_ACTIVE, 'Активна'),
        (STATUS_ARCHIVED, 'Архивирована'),
    ]
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    trained_at = models.DateTimeField('Дата обучения', null=True, blank=True)

    class Meta:
        verbose_name = 'Модель прогнозирования'
        verbose_name_plural = 'Модели прогнозирования'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_model_type_display()})"
