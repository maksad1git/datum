"""
API URLs for VISITS app
"""
from rest_framework.routers import DefaultRouter
from .api_views import (
    VisitTypeViewSet, VisitViewSet, ObservationViewSet,
    VisitMediaViewSet, SaleViewSet
)

router = DefaultRouter()
router.register(r'visit-types', VisitTypeViewSet, basename='visittype')
router.register(r'visits', VisitViewSet, basename='visit')
router.register(r'observations', ObservationViewSet, basename='observation')
router.register(r'visit-media', VisitMediaViewSet, basename='visitmedia')
router.register(r'sales', SaleViewSet, basename='sale')

urlpatterns = router.urls
