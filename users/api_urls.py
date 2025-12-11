"""
API URLs for USERS app
"""
from rest_framework.routers import DefaultRouter
from .api_views import RoleViewSet, PermissionViewSet, UserViewSet, UserSessionViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'users', UserViewSet, basename='user')
router.register(r'sessions', UserSessionViewSet, basename='usersession')

urlpatterns = router.urls
