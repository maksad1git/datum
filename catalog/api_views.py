"""
DRF ViewSets for CATALOG app
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Brand, Category, Product,
    AttributeGroup, AttributeDefinition, ProductAttributeValue,
    CategoryAttributeTemplate
)
from .serializers import (
    BrandSerializer, CategorySerializer, ProductSerializer,
    AttributeGroupSerializer, AttributeDefinitionSerializer,
    ProductAttributeValueSerializer, CategoryAttributeTemplateSerializer
)


class BrandViewSet(viewsets.ModelViewSet):
    """ViewSet for Brand model"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category model"""
    queryset = Category.objects.select_related('parent').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product model"""
    queryset = Product.objects.select_related('brand', 'category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['brand', 'category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class AttributeGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for AttributeGroup model"""
    queryset = AttributeGroup.objects.select_related('category').all()
    serializer_class = AttributeGroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'code']
    ordering_fields = ['order', 'name']
    ordering = ['order']


class AttributeDefinitionViewSet(viewsets.ModelViewSet):
    """ViewSet for AttributeDefinition model"""
    queryset = AttributeDefinition.objects.select_related('group').all()
    serializer_class = AttributeDefinitionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['group', 'data_type', 'is_active', 'is_required']
    search_fields = ['name', 'code']
    ordering_fields = ['order', 'name']
    ordering = ['order']


class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    """ViewSet for ProductAttributeValue model"""
    queryset = ProductAttributeValue.objects.select_related('product', 'attribute').all()
    serializer_class = ProductAttributeValueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'attribute']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class CategoryAttributeTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for CategoryAttributeTemplate model"""
    queryset = CategoryAttributeTemplate.objects.select_related('category', 'attribute').all()
    serializer_class = CategoryAttributeTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'attribute', 'is_required']
    ordering_fields = ['order']
    ordering = ['order']
