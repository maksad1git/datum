"""
API URLs for CATALOG app
"""
from rest_framework.routers import DefaultRouter
from .api_views import (
    BrandViewSet, CategoryViewSet, ProductViewSet,
    AttributeGroupViewSet, AttributeDefinitionViewSet,
    ProductAttributeValueViewSet, CategoryAttributeTemplateViewSet
)

router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'attribute-groups', AttributeGroupViewSet, basename='attributegroup')
router.register(r'attribute-definitions', AttributeDefinitionViewSet, basename='attributedefinition')
router.register(r'product-attributes', ProductAttributeValueViewSet, basename='productattributevalue')
router.register(r'category-templates', CategoryAttributeTemplateViewSet, basename='categoryattributetemplate')

urlpatterns = router.urls
