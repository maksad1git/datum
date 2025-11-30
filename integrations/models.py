from django.db import models
from django.conf import settings


class ImportJob(models.Model):
    """Задание на импорт данных"""
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)

    # Пользователь, запустивший импорт
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Создал',
        related_name='import_jobs'
    )

    # Источник данных
    SOURCE_FILE = 'file'
    SOURCE_API = 'api'
    SOURCE_DATABASE = 'database'
    SOURCE_1C = '1c'
    SOURCE_GOOGLE_SHEETS = 'google_sheets'
    SOURCE_CHOICES = [
        (SOURCE_FILE, 'Файл'),
        (SOURCE_API, 'API'),
        (SOURCE_DATABASE, 'База данных'),
        (SOURCE_1C, '1C'),
        (SOURCE_GOOGLE_SHEETS, 'Google Sheets'),
    ]
    source_type = models.CharField('Тип источника', max_length=50, choices=SOURCE_CHOICES, default=SOURCE_FILE)

    # Файл для импорта
    source_file = models.FileField('Файл источник', upload_to='imports/%Y/%m/', blank=True, null=True)
    source_url = models.URLField('URL источника', blank=True)

    # Тип импортируемых данных
    DATA_TYPE_OUTLETS = 'outlets'
    DATA_TYPE_PRODUCTS = 'products'
    DATA_TYPE_VISITS = 'visits'
    DATA_TYPE_OBSERVATIONS = 'observations'
    DATA_TYPE_COEFFICIENTS = 'coefficients'
    DATA_TYPE_CHOICES = [
        (DATA_TYPE_OUTLETS, 'Точки сбыта'),
        (DATA_TYPE_PRODUCTS, 'Товары'),
        (DATA_TYPE_VISITS, 'Визиты'),
        (DATA_TYPE_OBSERVATIONS, 'Наблюдения'),
        (DATA_TYPE_COEFFICIENTS, 'Коэффициенты'),
    ]
    data_type = models.CharField('Тип данных', max_length=50, choices=DATA_TYPE_CHOICES, default=DATA_TYPE_OUTLETS)

    # Формат данных
    FORMAT_CSV = 'csv'
    FORMAT_EXCEL = 'excel'
    FORMAT_JSON = 'json'
    FORMAT_XML = 'xml'
    FORMAT_CHOICES = [
        (FORMAT_CSV, 'CSV'),
        (FORMAT_EXCEL, 'Excel'),
        (FORMAT_JSON, 'JSON'),
        (FORMAT_XML, 'XML'),
    ]
    data_format = models.CharField('Формат данных', max_length=20, choices=FORMAT_CHOICES, default=FORMAT_CSV)

    # Настройки импорта
    mapping = models.JSONField(
        'Соответствие полей',
        default=dict,
        blank=True,
        help_text='Маппинг полей источника на поля модели'
    )
    options = models.JSONField('Опции импорта', default=dict, blank=True)

    # Статус
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_PARTIAL = 'partial'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидание'),
        (STATUS_PROCESSING, 'Обработка'),
        (STATUS_COMPLETED, 'Завершен'),
        (STATUS_FAILED, 'Ошибка'),
        (STATUS_PARTIAL, 'Частично завершен'),
    ]
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # Результаты импорта
    total_records = models.PositiveIntegerField('Всего записей', default=0)
    imported_records = models.PositiveIntegerField('Импортировано', default=0)
    failed_records = models.PositiveIntegerField('Ошибок', default=0)
    skipped_records = models.PositiveIntegerField('Пропущено', default=0)

    # Лог ошибок
    error_log = models.TextField('Лог ошибок', blank=True)
    error_file = models.FileField('Файл с ошибками', upload_to='imports/errors/', blank=True, null=True)

    # Время выполнения
    started_at = models.DateTimeField('Начало', null=True, blank=True)
    completed_at = models.DateTimeField('Окончание', null=True, blank=True)
    duration = models.FloatField('Длительность (сек)', null=True, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Задание импорта'
        verbose_name_plural = 'Задания импорта'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_by', '-created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    @property
    def success_rate(self):
        """Процент успешного импорта"""
        if self.total_records == 0:
            return 0
        return round((self.imported_records / self.total_records) * 100, 2)


class ExportJob(models.Model):
    """Задание на экспорт данных"""
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)

    # Пользователь, запустивший экспорт
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Создал',
        related_name='export_jobs'
    )

    # Тип экспортируемых данных
    DATA_TYPE_OUTLETS = 'outlets'
    DATA_TYPE_PRODUCTS = 'products'
    DATA_TYPE_VISITS = 'visits'
    DATA_TYPE_OBSERVATIONS = 'observations'
    DATA_TYPE_REPORT = 'report'
    DATA_TYPE_DASHBOARD = 'dashboard'
    DATA_TYPE_CHOICES = [
        (DATA_TYPE_OUTLETS, 'Точки сбыта'),
        (DATA_TYPE_PRODUCTS, 'Товары'),
        (DATA_TYPE_VISITS, 'Визиты'),
        (DATA_TYPE_OBSERVATIONS, 'Наблюдения'),
        (DATA_TYPE_REPORT, 'Отчет'),
        (DATA_TYPE_DASHBOARD, 'Дашборд'),
    ]
    data_type = models.CharField('Тип данных', max_length=50, choices=DATA_TYPE_CHOICES, default=DATA_TYPE_OUTLETS)

    # Формат экспорта
    FORMAT_CSV = 'csv'
    FORMAT_EXCEL = 'excel'
    FORMAT_JSON = 'json'
    FORMAT_XML = 'xml'
    FORMAT_PDF = 'pdf'
    FORMAT_CHOICES = [
        (FORMAT_CSV, 'CSV'),
        (FORMAT_EXCEL, 'Excel'),
        (FORMAT_JSON, 'JSON'),
        (FORMAT_XML, 'XML'),
        (FORMAT_PDF, 'PDF'),
    ]
    export_format = models.CharField('Формат экспорта', max_length=20, choices=FORMAT_CHOICES, default=FORMAT_EXCEL)

    # Фильтры для экспорта
    filters = models.JSONField('Фильтры', default=dict, blank=True)

    # Настройки экспорта
    options = models.JSONField(
        'Опции экспорта',
        default=dict,
        blank=True,
        help_text='Настройки формата, колонок и т.д.'
    )

    # Статус
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

    # Результат экспорта
    file = models.FileField('Файл результата', upload_to='exports/%Y/%m/', blank=True, null=True)
    total_records = models.PositiveIntegerField('Всего записей', default=0)
    file_size = models.PositiveIntegerField('Размер файла (байт)', default=0)

    # Лог ошибок
    error_log = models.TextField('Лог ошибок', blank=True)

    # Время выполнения
    started_at = models.DateTimeField('Начало', null=True, blank=True)
    completed_at = models.DateTimeField('Окончание', null=True, blank=True)
    duration = models.FloatField('Длительность (сек)', null=True, blank=True)

    # Срок хранения файла
    expires_at = models.DateTimeField('Срок хранения до', null=True, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Задание экспорта'
        verbose_name_plural = 'Задания экспорта'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_by', '-created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"


class Backup(models.Model):
    """Резервная копия данных"""
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)

    # Пользователь, создавший бэкап
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создал',
        related_name='backups'
    )

    # Тип бэкапа
    TYPE_FULL = 'full'
    TYPE_INCREMENTAL = 'incremental'
    TYPE_DIFFERENTIAL = 'differential'
    TYPE_MANUAL = 'manual'
    TYPE_CHOICES = [
        (TYPE_FULL, 'Полный'),
        (TYPE_INCREMENTAL, 'Инкрементный'),
        (TYPE_DIFFERENTIAL, 'Дифференциальный'),
        (TYPE_MANUAL, 'Ручной'),
    ]
    backup_type = models.CharField('Тип бэкапа', max_length=50, choices=TYPE_CHOICES, default=TYPE_FULL)

    # Что включено в бэкап
    includes_database = models.BooleanField('База данных', default=True)
    includes_media = models.BooleanField('Медиа файлы', default=False)
    includes_settings = models.BooleanField('Настройки', default=True)

    # Файл бэкапа
    file = models.FileField('Файл бэкапа', upload_to='backups/%Y/%m/', blank=True, null=True)
    file_size = models.BigIntegerField('Размер файла (байт)', default=0)
    checksum = models.CharField('Контрольная сумма', max_length=64, blank=True)

    # Метаданные бэкапа
    metadata = models.JSONField('Метаданные', default=dict, blank=True, help_text='Информация о содержимом бэкапа')

    # Статус
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидание'),
        (STATUS_IN_PROGRESS, 'Выполняется'),
        (STATUS_COMPLETED, 'Завершен'),
        (STATUS_FAILED, 'Ошибка'),
    ]
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # Время создания и срок хранения
    started_at = models.DateTimeField('Начало', null=True, blank=True)
    completed_at = models.DateTimeField('Окончание', null=True, blank=True)
    duration = models.FloatField('Длительность (сек)', null=True, blank=True)
    expires_at = models.DateTimeField('Срок хранения до', null=True, blank=True)

    # Информация о восстановлении
    is_restored = models.BooleanField('Восстановлен', default=False)
    restored_at = models.DateTimeField('Дата восстановления', null=True, blank=True)
    restored_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Восстановил',
        related_name='restored_backups'
    )

    # Лог ошибок
    error_log = models.TextField('Лог ошибок', blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Резервная копия'
        verbose_name_plural = 'Резервные копии'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['backup_type', '-created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def file_size_mb(self):
        """Размер файла в мегабайтах"""
        return round(self.file_size / (1024 * 1024), 2)
