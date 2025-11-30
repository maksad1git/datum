from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Role, User, Permission, UserSession


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_name_display', 'created_at', 'updated_at']
    list_filter = ['name', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    list_per_page = 25


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'status', 'is_staff']
    list_filter = ['status', 'role', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined', 'last_login_ip']
    ordering = ['-date_joined']
    list_per_page = 25
    date_hierarchy = 'date_joined'

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar')}),
        ('Permissions', {
            'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
        ('Additional info', {'fields': ('last_login_ip',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'status'),
        }),
    )


class PermissionInline(admin.TabularInline):
    model = Permission
    extra = 1
    fields = ['module', 'action', 'level']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'module', 'action', 'level', 'created_at']
    list_filter = ['action', 'level', 'role', 'created_at']
    search_fields = ['module', 'role__name']
    readonly_fields = ['created_at']
    ordering = ['role', 'module', 'action']
    list_per_page = 25
    date_hierarchy = 'created_at'


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'login_time', 'logout_time', 'is_active']
    list_filter = ['is_active', 'login_time', 'logout_time']
    search_fields = ['user__username', 'ip_address', 'session_key']
    readonly_fields = ['login_time']
    ordering = ['-login_time']
    list_per_page = 25
    date_hierarchy = 'login_time'
