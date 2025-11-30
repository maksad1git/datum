from django.db import models
from django.conf import settings


class FormTemplate(models.Model):
    """Шаблон формы - JSON конструктор динамических форм"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    # Тип формы
    TYPE_VISIT = 'visit'
    TYPE_SURVEY = 'survey'
    TYPE_AUDIT = 'audit'
    TYPE_REPORT = 'report'
    TYPE_OTHER = 'other'
    TYPE_CHOICES = [
        (TYPE_VISIT, 'Визит'),
        (TYPE_SURVEY, 'Опрос'),
        (TYPE_AUDIT, 'Аудит'),
        (TYPE_REPORT, 'Отчет'),
        (TYPE_OTHER, 'Другое'),
    ]
    form_type = models.CharField('Тип формы', max_length=50, choices=TYPE_CHOICES, default=TYPE_VISIT)

    # Структура формы в JSON
    # Пример: [
    #   {
    #     "field_name": "product_available",
    #     "field_type": "boolean",
    #     "label": "Товар в наличии",
    #     "required": true,
    #     "order": 1
    #   },
    #   {
    #     "field_name": "quantity",
    #     "field_type": "number",
    #     "label": "Количество",
    #     "required": false,
    #     "order": 2,
    #     "validation": {"min": 0}
    #   }
    # ]
    fields_schema = models.JSONField(
        'Схема полей',
        default=list,
        blank=True,
        help_text='JSON описание полей формы'
    )

    # Категория
    category = models.CharField('Категория', max_length=100, blank=True)

    # Версионирование
    version = models.CharField('Версия', max_length=20, default='1.0')
    parent_version = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Родительская версия',
        related_name='versions'
    )

    # Применимость
    applies_to_channels = models.ManyToManyField(
        'geo.Channel',
        verbose_name='Применяется к каналам',
        related_name='form_templates',
        blank=True
    )

    # Создатель
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создал',
        related_name='created_forms'
    )

    # Статус
    STATUS_DRAFT = 'draft'
    STATUS_ACTIVE = 'active'
    STATUS_ARCHIVED = 'archived'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_ACTIVE, 'Активен'),
        (STATUS_ARCHIVED, 'Архивирован'),
    ]
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    # Дополнительные настройки
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Шаблон формы'
        verbose_name_plural = 'Шаблоны форм'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['form_type', 'status']),
        ]

    def __str__(self):
        return f"{self.name} (v{self.version})"

    def get_active_version(self):
        """Получить активную версию формы"""
        return FormTemplate.objects.filter(
            code=self.code,
            status=self.STATUS_ACTIVE
        ).order_by('-version').first()
