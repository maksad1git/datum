"""
URL configuration for datum_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from core import views as core_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Главная страница
    path('', core_views.home, name='home'),

    # PWA Offline Page
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),

    # Админка
    path('admin/', admin.site.urls),

    # Авторизация
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # JWT Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # REST API endpoints (ALL 44 models!)
    path('api/v1/geo/', include('geo.api_urls')),
    path('api/v1/catalog/', include('catalog.api_urls')),
    path('api/v1/users/', include('users.api_urls')),
    path('api/v1/visits/', include('visits.api_urls')),
    path('api/v1/analytics/', include('analytics.api_urls')),
    path('api/v1/coefficients/', include('coefficients.api_urls')),
    path('api/v1/forms/', include('forms.api_urls')),
    path('api/v1/integrations/', include('integrations.api_urls')),
    path('api/v1/core/', include('core.api_urls'))

    # AJAX API (legacy - will be replaced by REST API)
    path('api/', include('api.urls')),

    # Traditional Django views (will be deprecated after Vue migration)
    path('users/', include('users.urls')),
    path('geo/', include('geo.urls')),
    path('catalog/', include('catalog.urls')),
    path('coefficients/', include('coefficients.urls')),
    path('visits/', include('visits.urls')),
    path('forms/', include('forms.urls')),
    path('analytics/', include('analytics.urls')),
    path('integrations/', include('integrations.urls')),
]

# Медиа файлы для разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
