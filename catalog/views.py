from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db import transaction

from .models import Brand, Category, Product
from .forms import BrandForm, CategoryForm, ProductForm, ProductAttributeValueFormSet


# ============================================================================
# Brand Views
# ============================================================================

class BrandListView(LoginRequiredMixin, ListView):
    model = Brand
    template_name = 'catalog/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 25

    def get_queryset(self):
        return Brand.objects.select_related('country')


class BrandDetailView(LoginRequiredMixin, DetailView):
    model = Brand
    template_name = 'catalog/brand_detail.html'
    context_object_name = 'brand'

    def get_queryset(self):
        return Brand.objects.select_related('country').prefetch_related('products')


class BrandCreateView(LoginRequiredMixin, CreateView):
    model = Brand
    template_name = 'catalog/brand_form.html'
    form_class = BrandForm
    success_url = reverse_lazy('catalog:brand_list')

    def form_valid(self, form):
        messages.success(self.request, f'Brand "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class BrandUpdateView(LoginRequiredMixin, UpdateView):
    model = Brand
    template_name = 'catalog/brand_form.html'
    form_class = BrandForm
    success_url = reverse_lazy('catalog:brand_list')

    def form_valid(self, form):
        messages.success(self.request, f'Brand "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class BrandDeleteView(LoginRequiredMixin, DeleteView):
    model = Brand
    template_name = 'catalog/brand_confirm_delete.html'
    success_url = reverse_lazy('catalog:brand_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Brand "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Category Views
# ============================================================================

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'
    paginate_by = 25

    def get_queryset(self):
        return Category.objects.select_related('parent')


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        return Category.objects.select_related('parent').prefetch_related('subcategories', 'products')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'catalog/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'catalog/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'catalog/category_confirm_delete.html'
    success_url = reverse_lazy('catalog:category_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Category "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Product Views
# ============================================================================

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 25

    def get_queryset(self):
        queryset = Product.objects.select_related('brand', 'category', 'brand__country')

        # Filter by brand
        brand_id = self.request.GET.get('brand')
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by attribute values
        for key, value in self.request.GET.items():
            if key.startswith('attr_') and value:
                attr_id = key.replace('attr_', '')
                try:
                    from .models import AttributeDefinition, ProductAttributeValue
                    attr_def = AttributeDefinition.objects.get(id=attr_id)

                    # Build filter based on attribute type
                    if attr_def.data_type == 'text':
                        product_ids = ProductAttributeValue.objects.filter(
                            attribute_id=attr_id,
                            value_text__icontains=value
                        ).values_list('product_id', flat=True)
                    elif attr_def.data_type == 'integer':
                        product_ids = ProductAttributeValue.objects.filter(
                            attribute_id=attr_id,
                            value_integer=int(value)
                        ).values_list('product_id', flat=True)
                    elif attr_def.data_type == 'decimal':
                        product_ids = ProductAttributeValue.objects.filter(
                            attribute_id=attr_id,
                            value_decimal=float(value)
                        ).values_list('product_id', flat=True)
                    elif attr_def.data_type == 'choice':
                        product_ids = ProductAttributeValue.objects.filter(
                            attribute_id=attr_id,
                            value_choice=value
                        ).values_list('product_id', flat=True)
                    else:
                        continue

                    queryset = queryset.filter(id__in=product_ids)
                except (AttributeDefinition.DoesNotExist, ValueError):
                    continue

        # Search by name or SKU
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(sku_code__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Brand, Category, AttributeDefinition

        # Add filter options
        context['brands'] = Brand.objects.all().order_by('name')
        context['categories'] = Category.objects.all().order_by('name')
        context['status_choices'] = Product.STATUS_CHOICES

        # Add filterable attributes
        context['filterable_attributes'] = AttributeDefinition.objects.filter(
            is_filterable=True,
            is_active=True
        ).select_related('group').order_by('group__order', 'order')

        # Preserve current filters
        current_filters = {
            'brand': self.request.GET.get('brand', ''),
            'category': self.request.GET.get('category', ''),
            'status': self.request.GET.get('status', ''),
            'search': self.request.GET.get('search', ''),
        }

        # Add attribute filter values
        for attr in context['filterable_attributes']:
            attr_key = f'attr_{attr.id}'
            current_filters[attr_key] = self.request.GET.get(attr_key, '')
            current_filters[f'{attr_key}_min'] = self.request.GET.get(f'{attr_key}_min', '')
            current_filters[f'{attr_key}_max'] = self.request.GET.get(f'{attr_key}_max', '')

        context['current_filters'] = current_filters

        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.select_related('brand', 'category', 'brand__country').prefetch_related(
            'attribute_values__attribute__group'
        )


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm

    def get_success_url(self):
        # После создания перенаправляем на редактирование для добавления атрибутов
        return reverse_lazy('catalog:product_update', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, f'Product "{form.instance.name}" created successfully. Now you can add attributes.')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['attribute_formset'] = ProductAttributeValueFormSet(self.request.POST, instance=self.object)
        else:
            context['attribute_formset'] = ProductAttributeValueFormSet(instance=self.object)
        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        attribute_formset = context['attribute_formset']

        if attribute_formset.is_valid():
            self.object = form.save()
            attribute_formset.instance = self.object
            attribute_formset.save()
            messages.success(self.request, f'Product "{form.instance.name}" updated successfully with attributes.')
            return super().form_valid(form)
        else:
            # Показать ошибки formset
            for i, form_errors in enumerate(attribute_formset.errors):
                if form_errors:
                    messages.error(self.request, f'Attribute form {i+1}: {form_errors}')
            if attribute_formset.non_form_errors():
                messages.error(self.request, f'Formset errors: {attribute_formset.non_form_errors()}')
            return self.render_to_response(self.get_context_data(form=form))


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Product "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# AJAX Endpoints
# ============================================================================

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import AttributeDefinition, AttributeGroup

@require_GET
def get_category_attributes(request, category_id):
    """
    AJAX endpoint для получения атрибутов категории
    Собирает атрибуты из текущей категории и всех родительских категорий
    """
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Категория не найдена'
        })

    # Собрать все категории в иерархии (текущая + все родительские)
    category_ids = []
    current = category
    while current is not None:
        category_ids.append(current.id)
        current = current.parent

    # Получить все группы атрибутов для категорий в иерархии
    groups = AttributeGroup.objects.filter(
        category_id__in=category_ids,
        is_active=True
    ).prefetch_related('attributes').order_by('order', 'name')

    # Собрать атрибуты
    attributes_data = []
    for group in groups:
        for attr in group.attributes.filter(is_active=True).order_by('order', 'name'):
            attributes_data.append({
                'id': attr.id,
                'name': attr.name,
                'code': attr.code,
                'data_type': attr.data_type,
                'group_name': group.name,
                'group_id': group.id,
                'is_required': attr.is_required,
                'is_filterable': attr.is_filterable,
                'choices': attr.choices if attr.data_type in ['choice', 'multi_choice'] else [],
                'unit': attr.unit,
                'help_text': attr.help_text,
            })

    return JsonResponse({
        'success': True,
        'attributes': attributes_data
    })


# ============================================================================
# AttributeGroup Views
# ============================================================================

class AttributeGroupListView(LoginRequiredMixin, ListView):
    model = AttributeGroup
    template_name = 'catalog/attributegroup_list.html'
    context_object_name = 'groups'
    paginate_by = 50

    def get_queryset(self):
        return AttributeGroup.objects.select_related('category').order_by('category__name', 'order', 'name')


class AttributeGroupDetailView(LoginRequiredMixin, DetailView):
    model = AttributeGroup
    template_name = 'catalog/attributegroup_detail.html'
    context_object_name = 'group'

    def get_queryset(self):
        return AttributeGroup.objects.select_related('category').prefetch_related('attributes')


class AttributeGroupCreateView(LoginRequiredMixin, CreateView):
    model = AttributeGroup
    template_name = 'catalog/attributegroup_form.html'
    fields = ['name', 'code', 'category', 'order', 'is_active']
    success_url = reverse_lazy('catalog:attributegroup_list')

    def form_valid(self, form):
        messages.success(self.request, f'Группа атрибутов "{form.instance.name}" создана успешно.')
        return super().form_valid(form)


class AttributeGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = AttributeGroup
    template_name = 'catalog/attributegroup_form.html'
    fields = ['name', 'code', 'category', 'order', 'is_active']
    success_url = reverse_lazy('catalog:attributegroup_list')

    def form_valid(self, form):
        messages.success(self.request, f'Группа атрибутов "{form.instance.name}" обновлена успешно.')
        return super().form_valid(form)


class AttributeGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = AttributeGroup
    template_name = 'catalog/attributegroup_confirm_delete.html'
    success_url = reverse_lazy('catalog:attributegroup_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Группа атрибутов "{self.get_object().name}" удалена успешно.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# AttributeDefinition Views
# ============================================================================

class AttributeDefinitionListView(LoginRequiredMixin, ListView):
    model = AttributeDefinition
    template_name = 'catalog/attributedefinition_list.html'
    context_object_name = 'attributes'
    paginate_by = 50

    def get_queryset(self):
        return AttributeDefinition.objects.select_related('group', 'group__category').order_by(
            'group__category__name', 'group__order', 'group__name', 'order', 'name'
        )


class AttributeDefinitionDetailView(LoginRequiredMixin, DetailView):
    model = AttributeDefinition
    template_name = 'catalog/attributedefinition_detail.html'
    context_object_name = 'attribute'

    def get_queryset(self):
        return AttributeDefinition.objects.select_related('group', 'group__category')


class AttributeDefinitionCreateView(LoginRequiredMixin, CreateView):
    model = AttributeDefinition
    template_name = 'catalog/attributedefinition_form.html'
    fields = [
        'name', 'code', 'group', 'data_type', 'is_required', 'is_filterable',
        'is_searchable', 'min_value', 'max_value', 'max_length', 'choices',
        'unit', 'placeholder', 'help_text', 'order', 'is_active'
    ]
    success_url = reverse_lazy('catalog:attributedefinition_list')

    def form_valid(self, form):
        messages.success(self.request, f'Атрибут "{form.instance.name}" создан успешно.')
        return super().form_valid(form)


class AttributeDefinitionUpdateView(LoginRequiredMixin, UpdateView):
    model = AttributeDefinition
    template_name = 'catalog/attributedefinition_form.html'
    fields = [
        'name', 'code', 'group', 'data_type', 'is_required', 'is_filterable',
        'is_searchable', 'min_value', 'max_value', 'max_length', 'choices',
        'unit', 'placeholder', 'help_text', 'order', 'is_active'
    ]
    success_url = reverse_lazy('catalog:attributedefinition_list')

    def form_valid(self, form):
        messages.success(self.request, f'Атрибут "{form.instance.name}" обновлён успешно.')
        return super().form_valid(form)


class AttributeDefinitionDeleteView(LoginRequiredMixin, DeleteView):
    model = AttributeDefinition
    template_name = 'catalog/attributedefinition_confirm_delete.html'
    success_url = reverse_lazy('catalog:attributedefinition_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Атрибут "{self.get_object().name}" удалён успешно.')
        return super().delete(request, *args, **kwargs)



# ============================================================================
# Preinstalled Categories Views
# ============================================================================

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .preinstall_loader import PreinstallLoader


@login_required
def preinstall_list(request):
    """Страница со списком предустановленных категорий"""
    presets = PreinstallLoader.get_available_presets()

    context = {
        'presets': presets,
    }

    return render(request, 'catalog/preinstall_list.html', context)


@login_required
def preinstall_load(request, filename):
    """Загрузить предустановленную категорию"""
    if request.method != 'POST':
        return redirect('catalog:preinstall_list')

    try:
        result = PreinstallLoader.load_preset(filename)

        messages.success(
            request,
            f'Категория "{result["meta"]["name"]}" успешно загружена! '
            f'Создано: {result["categories_created"]} категорий, '
            f'{result["groups_created"]} групп атрибутов, '
            f'{result["attributes_created"]} атрибутов.'
        )
    except FileNotFoundError:
        messages.error(request, f'Файл {filename} не найден')
    except ValueError as e:
        messages.warning(request, str(e))
    except Exception as e:
        messages.error(request, f'Ошибка при загрузке: {str(e)}')

    return redirect('catalog:preinstall_list')
