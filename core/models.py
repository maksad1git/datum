from django.db import models
from django.conf import settings


class SystemSettings(models.Model):
    """Глобальные настройки системы"""
    name = models.CharField('Название системы', max_length=255, default='Datum')
    logo = models.ImageField('Логотип', upload_to='system/', blank=True, null=True)
    currency = models.CharField('Валюта по умолчанию', max_length=10, default='USD')
    language = models.CharField('Язык', max_length=10, default='ru')
    timezone = models.CharField('Часовой пояс', max_length=50, default='Asia/Tashkent')

    # Единицы измерения
    UNIT_METRIC = 'metric'
    UNIT_IMPERIAL = 'imperial'
    UNIT_CHOICES = [
        (UNIT_METRIC, 'Метрическая'),
        (UNIT_IMPERIAL, 'Имперская'),
    ]
    unit_system = models.CharField('Система единиц', max_length=20, choices=UNIT_CHOICES, default=UNIT_METRIC)

    default_country = models.ForeignKey(
        'geo.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Страна по умолчанию'
    )

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Настройки системы'
        verbose_name_plural = 'Настройки системы'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Singleton pattern - только одна запись настроек
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class IntegrationSettings(models.Model):
    """Настройки интеграций с внешними системами"""
    TYPE_1C = '1c'
    TYPE_EXCEL = 'excel'
    TYPE_CRM = 'crm'
    TYPE_GOOGLE_SHEETS = 'google_sheets'
    TYPE_API = 'api'

    TYPE_CHOICES = [
        (TYPE_1C, '1C'),
        (TYPE_EXCEL, 'Excel'),
        (TYPE_CRM, 'CRM'),
        (TYPE_GOOGLE_SHEETS, 'Google Sheets'),
        (TYPE_API, 'API'),
    ]

    name = models.CharField('Название', max_length=255)
    type = models.CharField('Тип', max_length=50, choices=TYPE_CHOICES)
    api_key = models.CharField('API ключ', max_length=500, blank=True)
    endpoint_url = models.URLField('URL endpoint', blank=True)
    auth_params = models.JSONField('Параметры авторизации', default=dict, blank=True)
    is_active = models.BooleanField('Активно', default=True)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Настройки интеграции'
        verbose_name_plural = 'Настройки интеграций'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class SystemLog(models.Model):
    """Журнал системных событий"""
    LEVEL_INFO = 'info'
    LEVEL_WARNING = 'warning'
    LEVEL_ERROR = 'error'
    LEVEL_CRITICAL = 'critical'

    LEVEL_CHOICES = [
        (LEVEL_INFO, 'Информация'),
        (LEVEL_WARNING, 'Предупреждение'),
        (LEVEL_ERROR, 'Ошибка'),
        (LEVEL_CRITICAL, 'Критическая ошибка'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    level = models.CharField('Уровень', max_length=20, choices=LEVEL_CHOICES, default=LEVEL_INFO)
    action_type = models.CharField('Тип действия', max_length=100)
    description = models.TextField('Описание')
    ip_address = models.GenericIPAddressField('IP адрес', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Системный лог'
        verbose_name_plural = 'Системные логи'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.level.upper()}] {self.action_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class AuditLog(models.Model):
    """Журнал аудита изменений"""
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'

    ACTION_CHOICES = [
        (ACTION_CREATE, 'Создание'),
        (ACTION_UPDATE, 'Обновление'),
        (ACTION_DELETE, 'Удаление'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Пользователь'
    )
    action = models.CharField('Действие', max_length=20, choices=ACTION_CHOICES)
    table_name = models.CharField('Таблица', max_length=100)
    record_id = models.PositiveIntegerField('ID записи')
    old_value = models.JSONField('Старое значение', null=True, blank=True)
    new_value = models.JSONField('Новое значение', null=True, blank=True)
    timestamp = models.DateTimeField('Время', auto_now_add=True)
    ip_address = models.GenericIPAddressField('IP адрес', null=True, blank=True)

    class Meta:
        verbose_name = 'Запись аудита'
        verbose_name_plural = 'Журнал аудита'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['table_name', 'record_id']),
            models.Index(fields=['-timestamp']),
        ]

    def __str__(self):
        return f"{self.get_action_display()} {self.table_name}:{self.record_id} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
