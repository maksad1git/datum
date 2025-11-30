from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Dashboard URLs
    path('dashboards/', views.DashboardListView.as_view(), name='dashboard_list'),
    path('dashboards/<int:pk>/', views.DashboardDetailView.as_view(), name='dashboard_detail'),
    path('dashboards/create/', views.DashboardCreateView.as_view(), name='dashboard_create'),
    path('dashboards/<int:pk>/update/', views.DashboardUpdateView.as_view(), name='dashboard_update'),
    path('dashboards/<int:pk>/delete/', views.DashboardDeleteView.as_view(), name='dashboard_delete'),

    # Report URLs
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:pk>/pdf/', views.ReportPDFView.as_view(), name='report_pdf'),
    path('reports/<int:pk>/excel/', views.ReportExcelView.as_view(), name='report_excel'),
    path('reports/<int:pk>/csv/', views.ReportCSVView.as_view(), name='report_csv'),
    path('reports/create/', views.ReportCreateView.as_view(), name='report_create'),
    path('reports/<int:pk>/update/', views.ReportUpdateView.as_view(), name='report_update'),
    path('reports/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report_delete'),

    # ReportTemplate URLs
    path('reporttemplates/', views.ReportTemplateListView.as_view(), name='reporttemplate_list'),
    path('reporttemplates/<int:pk>/', views.ReportTemplateDetailView.as_view(), name='reporttemplate_detail'),
    path('reporttemplates/create/', views.ReportTemplateCreateView.as_view(), name='reporttemplate_create'),
    path('reporttemplates/<int:pk>/update/', views.ReportTemplateUpdateView.as_view(), name='reporttemplate_update'),
    path('reporttemplates/<int:pk>/delete/', views.ReportTemplateDeleteView.as_view(), name='reporttemplate_delete'),

    # FilterPreset URLs
    path('filterpresets/', views.FilterPresetListView.as_view(), name='filterpreset_list'),
    path('filterpresets/<int:pk>/', views.FilterPresetDetailView.as_view(), name='filterpreset_detail'),
    path('filterpresets/create/', views.FilterPresetCreateView.as_view(), name='filterpreset_create'),
    path('filterpresets/<int:pk>/update/', views.FilterPresetUpdateView.as_view(), name='filterpreset_update'),
    path('filterpresets/<int:pk>/delete/', views.FilterPresetDeleteView.as_view(), name='filterpreset_delete'),
]
