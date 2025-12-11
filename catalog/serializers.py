"""
DRF Serializers for CATALOG app models
"""
from rest_framework import serializers
from .models import (
    Brand, Category, Product,
    AttributeGroup, AttributeDefinition, ProductAttributeValue,
    CategoryAttributeTemplate
)


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for Brand model"""

    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    parent_name = serializers.CharField(source='parent.name', read_only=True, allow_null=True)

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""
    brand_name = serializers.CharField(source='brand.name', read_only=True, allow_null=True)
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)

    class Meta:
        model = Product
        fields = '__all__'


class AttributeGroupSerializer(serializers.ModelSerializer):
    """Serializer for AttributeGroup model"""
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)

    class Meta:
        model = AttributeGroup
        fields = '__all__'


class AttributeDefinitionSerializer(serializers.ModelSerializer):
    """Serializer for AttributeDefinition model"""
    group_name = serializers.CharField(source='group.name', read_only=True, allow_null=True)

    class Meta:
        model = AttributeDefinition
        fields = '__all__'


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """Serializer for ProductAttributeValue model"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = '__all__'


class CategoryAttributeTemplateSerializer(serializers.ModelSerializer):
    """Serializer for CategoryAttributeTemplate model"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = CategoryAttributeTemplate
        fields = '__all__'
