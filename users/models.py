from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    """Роли пользователей"""
    ADMIN = 'admin'
    ANALYST = 'analyst'
    EXPERT = 'expert'
    INSPECTOR = 'inspector'

    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (ANALYST, 'Аналитик'),
        (EXPERT, 'Эксперт'),
        (INSPECTOR, 'Инспектор'),
    ]

    name = models.CharField('Название', max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    """Кастомная модель пользователя"""
    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'
    STATUS_INACTIVE = 'inactive'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Активен'),
        (STATUS_SUSPENDED, 'Приостановлен'),
        (STATUS_INACTIVE, 'Неактивен'),
    ]

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Роль',
        related_name='users'
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )
    phone = models.CharField('Телефон', max_length=20, blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)

    # Дополнительные метаданные
    last_login_ip = models.GenericIPAddressField('IP последнего входа', null=True, blank=True)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})" if self.role else self.username


class Permission(models.Model):
    """Права доступа"""
    ACTION_VIEW = 'view'
    ACTION_CREATE = 'create'
    ACTION_EDIT = 'edit'
    ACTION_DELETE = 'delete'

    ACTION_CHOICES = [
        (ACTION_VIEW, 'Просмотр'),
        (ACTION_CREATE, 'Создание'),
        (ACTION_EDIT, 'Редактирование'),
        (ACTION_DELETE, 'Удаление'),
    ]

    LEVEL_MON = 'monitoring'
    LEVEL_EXP = 'expertise'
    LEVEL_BOTH = 'both'

    LEVEL_CHOICES = [
        (LEVEL_MON, 'Monitoring'),
        (LEVEL_EXP, 'Expertise'),
        (LEVEL_BOTH, 'Оба типа'),
    ]

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name='Роль',
        related_name='permissions'
    )
    module = models.CharField('Модуль (app)', max_length=100)
    action = models.CharField('Действие', max_length=20, choices=ACTION_CHOICES)
    level = models.CharField('Уровень данных', max_length=20, choices=LEVEL_CHOICES, default=LEVEL_BOTH)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Право доступа'
        verbose_name_plural = 'Права доступа'
        ordering = ['role', 'module', 'action']
        unique_together = ['role', 'module', 'action', 'level']

    def __str__(self):
        return f"{self.role} - {self.module} - {self.get_action_display()}"


class UserSession(models.Model):
    """Сессии пользователей"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='sessions'
    )
    session_key = models.CharField('Ключ сессии', max_length=255, unique=True)
    ip_address = models.GenericIPAddressField('IP адрес', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    login_time = models.DateTimeField('Время входа', auto_now_add=True)
    logout_time = models.DateTimeField('Время выхода', null=True, blank=True)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Сессия пользователя'
        verbose_name_plural = 'Сессии пользователей'
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} - {self.login_time.strftime('%Y-%m-%d %H:%M')}"
