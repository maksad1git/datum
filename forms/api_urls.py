from rest_framework.routers import DefaultRouter
from .api_views import FormTemplateViewSet

router = DefaultRouter()
router.register(r'form-templates', FormTemplateViewSet, basename='formtemplate')
urlpatterns = router.urls
