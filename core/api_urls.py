from rest_framework.routers import DefaultRouter
from .api_views import SystemSettingsViewSet, IntegrationSettingsViewSet, SystemLogViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'system-settings', SystemSettingsViewSet, basename='systemsettings')
router.register(r'integration-settings', IntegrationSettingsViewSet, basename='integrationsettings')
router.register(r'system-logs', SystemLogViewSet, basename='systemlog')
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')
urlpatterns = router.urls
