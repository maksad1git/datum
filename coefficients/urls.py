from django.urls import path
from . import views

app_name = 'coefficients'

urlpatterns = [
    # Coefficient URLs
    path('coefficients/', views.CoefficientListView.as_view(), name='coefficient_list'),
    path('coefficients/<int:pk>/', views.CoefficientDetailView.as_view(), name='coefficient_detail'),
    path('coefficients/create/', views.CoefficientCreateView.as_view(), name='coefficient_create'),
    path('coefficients/<int:pk>/update/', views.CoefficientUpdateView.as_view(), name='coefficient_update'),
    path('coefficients/<int:pk>/delete/', views.CoefficientDeleteView.as_view(), name='coefficient_delete'),

    # Metric URLs
    path('metrics/', views.MetricListView.as_view(), name='metric_list'),
    path('metrics/<int:pk>/', views.MetricDetailView.as_view(), name='metric_detail'),
    path('metrics/create/', views.MetricCreateView.as_view(), name='metric_create'),
    path('metrics/<int:pk>/update/', views.MetricUpdateView.as_view(), name='metric_update'),
    path('metrics/<int:pk>/delete/', views.MetricDeleteView.as_view(), name='metric_delete'),

    # Formula URLs
    path('formulas/', views.FormulaListView.as_view(), name='formula_list'),
    path('formulas/<int:pk>/', views.FormulaDetailView.as_view(), name='formula_detail'),
    path('formulas/create/', views.FormulaCreateView.as_view(), name='formula_create'),
    path('formulas/<int:pk>/update/', views.FormulaUpdateView.as_view(), name='formula_update'),
    path('formulas/<int:pk>/delete/', views.FormulaDeleteView.as_view(), name='formula_delete'),

    # Rule URLs
    path('rules/', views.RuleListView.as_view(), name='rule_list'),
    path('rules/<int:pk>/', views.RuleDetailView.as_view(), name='rule_detail'),
    path('rules/create/', views.RuleCreateView.as_view(), name='rule_create'),
    path('rules/<int:pk>/update/', views.RuleUpdateView.as_view(), name='rule_update'),
    path('rules/<int:pk>/delete/', views.RuleDeleteView.as_view(), name='rule_delete'),
]
