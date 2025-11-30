from django.urls import path
from . import views

app_name = 'forms'

urlpatterns = [
    # FormTemplate URLs
    path('', views.FormTemplateListView.as_view(), name='formtemplate_list'),
    path('<int:pk>/', views.FormTemplateDetailView.as_view(), name='formtemplate_detail'),
    path('create/', views.FormTemplateCreateView.as_view(), name='formtemplate_create'),
    path('<int:pk>/update/', views.FormTemplateUpdateView.as_view(), name='formtemplate_update'),
    path('<int:pk>/delete/', views.FormTemplateDeleteView.as_view(), name='formtemplate_delete'),
]
