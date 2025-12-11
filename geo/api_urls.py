"""
API URLs for GEO app
"""
from rest_framework.routers import DefaultRouter
from .api_views import (
    GlobalMarketViewSet, CountryViewSet, RegionViewSet,
    CityViewSet, DistrictViewSet, ChannelViewSet, OutletViewSet,
    FootfallCounterViewSet, OutletInventoryViewSet,
    DisplayViewSet, DisplayInventoryViewSet
)

router = DefaultRouter()
router.register(r'globalmarkets', GlobalMarketViewSet, basename='globalmarket')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'channels', ChannelViewSet, basename='channel')
router.register(r'outlets', OutletViewSet, basename='outlet')
router.register(r'footfall-counters', FootfallCounterViewSet, basename='footfallcounter')
router.register(r'outlet-inventory', OutletInventoryViewSet, basename='outletinventory')
router.register(r'displays', DisplayViewSet, basename='display')
router.register(r'display-inventory', DisplayInventoryViewSet, basename='displayinventory')

urlpatterns = router.urls
