"""
API URLs for ANALYTICS app
"""
from rest_framework.routers import DefaultRouter
from .api_views import (
    DashboardViewSet, ReportViewSet, ReportTemplateViewSet,
    FilterPresetViewSet, ForecastModelViewSet
)

router = DefaultRouter()
router.register(r'dashboards', DashboardViewSet, basename='dashboard')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'report-templates', ReportTemplateViewSet, basename='reporttemplate')
router.register(r'filter-presets', FilterPresetViewSet, basename='filterpreset')
router.register(r'forecast-models', ForecastModelViewSet, basename='forecastmodel')

urlpatterns = router.urls
