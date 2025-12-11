from rest_framework.routers import DefaultRouter
from .api_views import ImportJobViewSet, ExportJobViewSet, BackupViewSet

router = DefaultRouter()
router.register(r'import-jobs', ImportJobViewSet, basename='importjob')
router.register(r'export-jobs', ExportJobViewSet, basename='exportjob')
router.register(r'backups', BackupViewSet, basename='backup')
urlpatterns = router.urls
