from django.urls import path
from . import views

app_name = 'visits'

urlpatterns = [
    # VisitType URLs
    path('visittypes/', views.VisitTypeListView.as_view(), name='visittype_list'),
    path('visittypes/<int:pk>/', views.VisitTypeDetailView.as_view(), name='visittype_detail'),
    path('visittypes/create/', views.VisitTypeCreateView.as_view(), name='visittype_create'),
    path('visittypes/<int:pk>/update/', views.VisitTypeUpdateView.as_view(), name='visittype_update'),
    path('visittypes/<int:pk>/delete/', views.VisitTypeDeleteView.as_view(), name='visittype_delete'),

    # Visit URLs
    path('', views.VisitListView.as_view(), name='visit_list'),
    path('<int:pk>/', views.VisitDetailView.as_view(), name='visit_detail'),
    path('create/', views.VisitCreateView.as_view(), name='visit_create'),
    path('<int:pk>/update/', views.VisitUpdateView.as_view(), name='visit_update'),
    path('<int:pk>/delete/', views.VisitDeleteView.as_view(), name='visit_delete'),

    # Интерфейс для тайного покупателя
    path('my-visits/', views.my_visits, name='my_visits'),
    path('start-now/', views.start_visit_now, name='start_visit_now'),
    path('quick-start/', views.quick_start_visit, name='quick_start_visit'),
    path('<int:pk>/fill/', views.fill_visit, name='fill_visit'),

    # Observation URLs
    path('observations/', views.ObservationListView.as_view(), name='observation_list'),
    path('observations/<int:pk>/', views.ObservationDetailView.as_view(), name='observation_detail'),
    path('observations/create/', views.ObservationCreateView.as_view(), name='observation_create'),
    path('observations/<int:pk>/update/', views.ObservationUpdateView.as_view(), name='observation_update'),
    path('observations/<int:pk>/delete/', views.ObservationDeleteView.as_view(), name='observation_delete'),

    # VisitMedia URLs
    path('media/', views.VisitMediaListView.as_view(), name='visitmedia_list'),
    path('media/<int:pk>/', views.VisitMediaDetailView.as_view(), name='visitmedia_detail'),
    path('media/create/', views.VisitMediaCreateView.as_view(), name='visitmedia_create'),
    path('media/<int:pk>/update/', views.VisitMediaUpdateView.as_view(), name='visitmedia_update'),
    path('media/<int:pk>/delete/', views.VisitMediaDeleteView.as_view(), name='visitmedia_delete'),

    # API для Background Sync
    path('api/sync/', views.sync_visit_api, name='sync_visit_api'),
]
