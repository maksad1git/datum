from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Brand URLs
    path('brands/', views.BrandListView.as_view(), name='brand_list'),
    path('brands/<int:pk>/', views.BrandDetailView.as_view(), name='brand_detail'),
    path('brands/create/', views.BrandCreateView.as_view(), name='brand_create'),
    path('brands/<int:pk>/update/', views.BrandUpdateView.as_view(), name='brand_update'),
    path('brands/<int:pk>/delete/', views.BrandDeleteView.as_view(), name='brand_delete'),

    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # Product URLs
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # AttributeGroup URLs
    path('attribute-groups/', views.AttributeGroupListView.as_view(), name='attributegroup_list'),
    path('attribute-groups/<int:pk>/', views.AttributeGroupDetailView.as_view(), name='attributegroup_detail'),
    path('attribute-groups/create/', views.AttributeGroupCreateView.as_view(), name='attributegroup_create'),
    path('attribute-groups/<int:pk>/update/', views.AttributeGroupUpdateView.as_view(), name='attributegroup_update'),
    path('attribute-groups/<int:pk>/delete/', views.AttributeGroupDeleteView.as_view(), name='attributegroup_delete'),

    # AttributeDefinition URLs
    path('attributes/', views.AttributeDefinitionListView.as_view(), name='attributedefinition_list'),
    path('attributes/<int:pk>/', views.AttributeDefinitionDetailView.as_view(), name='attributedefinition_detail'),
    path('attributes/create/', views.AttributeDefinitionCreateView.as_view(), name='attributedefinition_create'),
    path('attributes/<int:pk>/update/', views.AttributeDefinitionUpdateView.as_view(), name='attributedefinition_update'),
    path('attributes/<int:pk>/delete/', views.AttributeDefinitionDeleteView.as_view(), name='attributedefinition_delete'),

    # AJAX endpoints
    path('ajax/category/<int:category_id>/attributes/', views.get_category_attributes, name='category_attributes'),

    # Preinstalled categories
    path('preinstall/', views.preinstall_list, name='preinstall_list'),
    path('preinstall/load/<str:filename>/', views.preinstall_load, name='preinstall_load'),
]
