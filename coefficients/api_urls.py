"""
API URLs for COEFFICIENTS app
"""
from rest_framework.routers import DefaultRouter
from .api_views import CoefficientViewSet, MetricViewSet, FormulaViewSet, RuleViewSet

router = DefaultRouter()
router.register(r'coefficients', CoefficientViewSet, basename='coefficient')
router.register(r'metrics', MetricViewSet, basename='metric')
router.register(r'formulas', FormulaViewSet, basename='formula')
router.register(r'rules', RuleViewSet, basename='rule')

urlpatterns = router.urls
