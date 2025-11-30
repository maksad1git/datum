from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Coefficient, Metric, Formula, Rule
from .forms import CoefficientForm, MetricForm, FormulaForm, RuleForm


# ============================================================================
# Coefficient Views
# ============================================================================

class CoefficientListView(LoginRequiredMixin, ListView):
    model = Coefficient
    template_name = 'coefficients/coefficient_list.html'
    context_object_name = 'coefficients'
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset()
        data_type = self.request.GET.get('data_type')
        if data_type in ['MON', 'EXP', 'AI']:
            queryset = queryset.filter(data_type=data_type)
        return queryset


class CoefficientDetailView(LoginRequiredMixin, DetailView):
    model = Coefficient
    template_name = 'coefficients/coefficient_detail.html'
    context_object_name = 'coefficient'

    def get_queryset(self):
        return Coefficient.objects.prefetch_related('metrics', 'formulas', 'rules')


class CoefficientCreateView(LoginRequiredMixin, CreateView):
    model = Coefficient
    template_name = 'coefficients/coefficient_form.html'
    form_class = CoefficientForm
    success_url = reverse_lazy('coefficients:coefficient_list')

    def form_valid(self, form):
        messages.success(self.request, f'Coefficient "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class CoefficientUpdateView(LoginRequiredMixin, UpdateView):
    model = Coefficient
    template_name = 'coefficients/coefficient_form.html'
    form_class = CoefficientForm
    success_url = reverse_lazy('coefficients:coefficient_list')

    def form_valid(self, form):
        messages.success(self.request, f'Coefficient "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class CoefficientDeleteView(LoginRequiredMixin, DeleteView):
    model = Coefficient
    template_name = 'coefficients/coefficient_confirm_delete.html'
    success_url = reverse_lazy('coefficients:coefficient_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Coefficient "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Metric Views
# ============================================================================

class MetricListView(LoginRequiredMixin, ListView):
    model = Metric
    template_name = 'coefficients/metric_list.html'
    context_object_name = 'metrics'
    paginate_by = 25

    def get_queryset(self):
        return Metric.objects.select_related('formula')


class MetricDetailView(LoginRequiredMixin, DetailView):
    model = Metric
    template_name = 'coefficients/metric_detail.html'
    context_object_name = 'metric'

    def get_queryset(self):
        return Metric.objects.select_related('formula').prefetch_related('coefficients')


class MetricCreateView(LoginRequiredMixin, CreateView):
    model = Metric
    template_name = 'coefficients/metric_form.html'
    form_class = MetricForm
    success_url = reverse_lazy('coefficients:metric_list')

    def form_valid(self, form):
        messages.success(self.request, f'Metric "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class MetricUpdateView(LoginRequiredMixin, UpdateView):
    model = Metric
    template_name = 'coefficients/metric_form.html'
    form_class = MetricForm
    success_url = reverse_lazy('coefficients:metric_list')

    def form_valid(self, form):
        messages.success(self.request, f'Metric "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class MetricDeleteView(LoginRequiredMixin, DeleteView):
    model = Metric
    template_name = 'coefficients/metric_confirm_delete.html'
    success_url = reverse_lazy('coefficients:metric_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Metric "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Formula Views
# ============================================================================

class FormulaListView(LoginRequiredMixin, ListView):
    model = Formula
    template_name = 'coefficients/formula_list.html'
    context_object_name = 'formulas'
    paginate_by = 25


class FormulaDetailView(LoginRequiredMixin, DetailView):
    model = Formula
    template_name = 'coefficients/formula_detail.html'
    context_object_name = 'formula'

    def get_queryset(self):
        return Formula.objects.prefetch_related('coefficients', 'metrics')


class FormulaCreateView(LoginRequiredMixin, CreateView):
    model = Formula
    template_name = 'coefficients/formula_form.html'
    form_class = FormulaForm
    success_url = reverse_lazy('coefficients:formula_list')

    def form_valid(self, form):
        messages.success(self.request, f'Formula "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class FormulaUpdateView(LoginRequiredMixin, UpdateView):
    model = Formula
    template_name = 'coefficients/formula_form.html'
    form_class = FormulaForm
    success_url = reverse_lazy('coefficients:formula_list')

    def form_valid(self, form):
        messages.success(self.request, f'Formula "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class FormulaDeleteView(LoginRequiredMixin, DeleteView):
    model = Formula
    template_name = 'coefficients/formula_confirm_delete.html'
    success_url = reverse_lazy('coefficients:formula_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Formula "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# Rule Views
# ============================================================================

class RuleListView(LoginRequiredMixin, ListView):
    model = Rule
    template_name = 'coefficients/rule_list.html'
    context_object_name = 'rules'
    paginate_by = 25


class RuleDetailView(LoginRequiredMixin, DetailView):
    model = Rule
    template_name = 'coefficients/rule_detail.html'
    context_object_name = 'rule'

    def get_queryset(self):
        return Rule.objects.prefetch_related('applies_to')


class RuleCreateView(LoginRequiredMixin, CreateView):
    model = Rule
    template_name = 'coefficients/rule_form.html'
    form_class = RuleForm
    success_url = reverse_lazy('coefficients:rule_list')

    def form_valid(self, form):
        messages.success(self.request, f'Rule "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class RuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Rule
    template_name = 'coefficients/rule_form.html'
    form_class = RuleForm
    success_url = reverse_lazy('coefficients:rule_list')

    def form_valid(self, form):
        messages.success(self.request, f'Rule "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class RuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Rule
    template_name = 'coefficients/rule_confirm_delete.html'
    success_url = reverse_lazy('coefficients:rule_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Rule "{self.get_object().name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# API для визуального конструктора
# ============================================================================

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def coefficients_api(request):
    """API для получения списка коэффициентов (для визуального конструктора)"""
    coefficients = Coefficient.objects.filter(is_active=True).values('id', 'name', 'code', 'unit', 'value_type')
    return JsonResponse(list(coefficients), safe=False)
