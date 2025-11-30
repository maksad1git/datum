from django.db import models
from django.conf import settings
from core.constants import DATA_SOURCE_CHOICES


class VisitType(models.Model):
    """Тип визита - шаблон для проведения визитов"""
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    # Связь с формой
    form_template = models.ForeignKey(
        'forms.FormTemplate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Шаблон формы',
        related_name='visit_types'
    )

    # Применимые коэффициенты
    coefficients = models.ManyToManyField(
        'coefficients.Coefficient',
        verbose_name='Коэффициенты',
        related_name='visit_types',
        blank=True
    )

    # Тип визита
    TYPE_MONITORING = 'monitoring'
    TYPE_AUDIT = 'audit'
    TYPE_SURVEY = 'survey'
    TYPE_INSPECTION = 'inspection'
    TYPE_OTHER = 'other'
    TYPE_CHOICES = [
        (TYPE_MONITORING, 'Мониторинг'),
        (TYPE_AUDIT, 'Аудит'),
        (TYPE_SURVEY, 'Опрос'),
        (TYPE_INSPECTION, 'Инспекция'),
        (TYPE_OTHER, 'Другое'),
    ]
    type = models.CharField('Тип', max_length=50, choices=TYPE_CHOICES, default=TYPE_MONITORING)

    # Требования
    requires_photo = models.BooleanField('Требует фото', default=False)
    requires_signature = models.BooleanField('Требует подпись', default=False)
    requires_gps = models.BooleanField('Требует GPS координаты', default=False)

    # Статус
    is_active = models.BooleanField('Активен', default=True)

    # Дополнительные параметры
    settings = models.JSONField('Дополнительные настройки', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Тип визита'
        verbose_name_plural = 'Типы визитов'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Visit(models.Model):
    """Визит - посещение точки сбыта"""
    visit_type = models.ForeignKey(
        VisitType,
        on_delete=models.CASCADE,
        verbose_name='Тип визита',
        related_name='visits'
    )
    outlet = models.ForeignKey(
        'geo.Outlet',
        on_delete=models.CASCADE,
        verbose_name='Точка сбыта',
        related_name='visits'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Исполнитель',
        related_name='visits'
    )

    # Даты и время
    planned_date = models.DateTimeField('Плановая дата', null=True, blank=True)
    start_date = models.DateTimeField('Дата начала', null=True, blank=True)
    end_date = models.DateTimeField('Дата окончания', null=True, blank=True)

    # Статус визита
    STATUS_PLANNED = 'planned'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PLANNED, 'Запланирован'),
        (STATUS_IN_PROGRESS, 'В процессе'),
        (STATUS_COMPLETED, 'Завершен'),
        (STATUS_CANCELLED, 'Отменен'),
    ]
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_PLANNED)

    # GPS координаты (заглушка на потом)
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6, null=True, blank=True)

    # Тип источника данных для визита
    data_source_type = models.CharField(
        'Тип визита',
        max_length=10,
        choices=DATA_SOURCE_CHOICES,
        default='MON',
        help_text='Тип визита: мониторинговый (замеры) или экспертный (интервью)'
    )

    # Комментарии
    notes = models.TextField('Комментарии', blank=True)

    # Гибкие данные (результаты формы в JSON)
    form_data = models.JSONField('Данные формы', default=dict, blank=True)

    # Подпись
    signature = models.ImageField('Подпись', upload_to='signatures/', blank=True, null=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Визит'
        verbose_name_plural = 'Визиты'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['outlet', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.visit_type.name} - {self.outlet.name} ({self.created_at.strftime('%Y-%m-%d')})"


class Observation(models.Model):
    """Наблюдение - единичный замер коэффициента во время визита"""
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        verbose_name='Визит',
        related_name='observations'
    )
    coefficient = models.ForeignKey(
        'coefficients.Coefficient',
        on_delete=models.CASCADE,
        verbose_name='Коэффициент',
        related_name='observations'
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Товар',
        related_name='observations'
    )

    # Тип источника данных для наблюдения
    data_source_type = models.CharField(
        'Тип источника данных',
        max_length=10,
        choices=DATA_SOURCE_CHOICES,
        default='MON',
        help_text='Как получено это наблюдение: замер, от эксперта или ИИ'
    )

    # Значения (гибкая структура)
    value_numeric = models.DecimalField('Числовое значение', max_digits=15, decimal_places=4, null=True, blank=True)
    value_text = models.TextField('Текстовое значение', blank=True)
    value_boolean = models.BooleanField('Да/Нет значение', null=True, blank=True)

    # Дополнительные данные
    notes = models.TextField('Комментарии', blank=True)
    metadata = models.JSONField('Метаданные', default=dict, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Наблюдение'
        verbose_name_plural = 'Наблюдения'
        ordering = ['visit', 'coefficient']
        indexes = [
            models.Index(fields=['visit', 'coefficient']),
            models.Index(fields=['coefficient', 'product']),
        ]

    def __str__(self):
        product_str = f" ({self.product.name})" if self.product else ""
        return f"{self.coefficient.name}{product_str} - {self.visit.outlet.name}"

    def get_value(self):
        """Получить значение в зависимости от типа коэффициента"""
        if self.coefficient.value_type == 'numeric':
            return self.value_numeric
        elif self.coefficient.value_type == 'boolean':
            return self.value_boolean
        else:
            return self.value_text


class VisitMedia(models.Model):
    """Медиа файлы визита (фото/видео)"""
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        verbose_name='Визит',
        related_name='media'
    )
    observation = models.ForeignKey(
        Observation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Наблюдение',
        related_name='media'
    )

    # Тип медиа
    TYPE_PHOTO = 'photo'
    TYPE_VIDEO = 'video'
    TYPE_AUDIO = 'audio'
    TYPE_DOCUMENT = 'document'
    TYPE_CHOICES = [
        (TYPE_PHOTO, 'Фото'),
        (TYPE_VIDEO, 'Видео'),
        (TYPE_AUDIO, 'Аудио'),
        (TYPE_DOCUMENT, 'Документ'),
    ]
    media_type = models.CharField('Тип медиа', max_length=20, choices=TYPE_CHOICES, default=TYPE_PHOTO)

    # Файл
    file = models.FileField('Файл', upload_to='visit_media/%Y/%m/%d/')
    thumbnail = models.ImageField('Миниатюра', upload_to='visit_media/thumbnails/', blank=True, null=True)

    # Описание
    title = models.CharField('Название', max_length=255, blank=True)
    description = models.TextField('Описание', blank=True)

    # EXIF данные (заглушка на потом)
    exif_data = models.JSONField('EXIF данные', default=dict, blank=True)

    # GPS из EXIF (заглушка)
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6, null=True, blank=True)

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Медиа файл визита'
        verbose_name_plural = 'Медиа файлы визитов'
        ordering = ['visit', 'created_at']

    def __str__(self):
        return f"{self.get_media_type_display()} - {self.visit.outlet.name}"


class Sale(models.Model):
    """Продажа товара"""
    outlet = models.ForeignKey(
        'geo.Outlet',
        on_delete=models.CASCADE,
        verbose_name='Торговая точка',
        related_name='sales'
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='sales'
    )
    quantity = models.IntegerField(verbose_name="Количество")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за единицу"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Сумма"
    )
    sale_date = models.DateTimeField(verbose_name="Дата продажи")
    recorded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Зафиксировано"
    )
    recorded_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Зафиксировал"
    )

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
        ordering = ['-sale_date']

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт x {self.price}₽ = {self.total_amount}₽"
