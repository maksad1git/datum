from django.urls import path
from . import views

app_name = 'integrations'

urlpatterns = [
    # ImportJob URLs
    path('imports/', views.ImportJobListView.as_view(), name='importjob_list'),
    path('imports/<int:pk>/', views.ImportJobDetailView.as_view(), name='importjob_detail'),
    path('imports/create/', views.ImportJobCreateView.as_view(), name='importjob_create'),
    path('imports/<int:pk>/update/', views.ImportJobUpdateView.as_view(), name='importjob_update'),
    path('imports/<int:pk>/delete/', views.ImportJobDeleteView.as_view(), name='importjob_delete'),

    # ExportJob URLs
    path('exports/', views.ExportJobListView.as_view(), name='exportjob_list'),
    path('exports/<int:pk>/', views.ExportJobDetailView.as_view(), name='exportjob_detail'),
    path('exports/create/', views.ExportJobCreateView.as_view(), name='exportjob_create'),
    path('exports/<int:pk>/update/', views.ExportJobUpdateView.as_view(), name='exportjob_update'),
    path('exports/<int:pk>/delete/', views.ExportJobDeleteView.as_view(), name='exportjob_delete'),

    # Backup URLs
    path('backups/', views.BackupListView.as_view(), name='backup_list'),
    path('backups/<int:pk>/', views.BackupDetailView.as_view(), name='backup_detail'),
    path('backups/create/', views.BackupCreateView.as_view(), name='backup_create'),
    path('backups/<int:pk>/update/', views.BackupUpdateView.as_view(), name='backup_update'),
    path('backups/<int:pk>/delete/', views.BackupDeleteView.as_view(), name='backup_delete'),
]
