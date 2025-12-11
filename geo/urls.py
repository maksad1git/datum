from django.urls import path
from . import views

app_name = 'geo'

urlpatterns = [
    # GlobalMarket URLs
    path('globalmarkets/', views.GlobalMarketListView.as_view(), name='globalmarket_list'),
    path('globalmarkets/<int:pk>/', views.GlobalMarketDetailView.as_view(), name='globalmarket_detail'),
    path('globalmarkets/create/', views.GlobalMarketCreateView.as_view(), name='globalmarket_create'),
    path('globalmarkets/<int:pk>/update/', views.GlobalMarketUpdateView.as_view(), name='globalmarket_update'),
    path('globalmarkets/<int:pk>/delete/', views.GlobalMarketDeleteView.as_view(), name='globalmarket_delete'),

    # Country URLs
    path('countries/', views.CountryListView.as_view(), name='country_list'),
    path('countries/<int:pk>/', views.CountryDetailView.as_view(), name='country_detail'),
    path('countries/create/', views.CountryCreateView.as_view(), name='country_create'),
    path('countries/<int:pk>/update/', views.CountryUpdateView.as_view(), name='country_update'),
    path('countries/<int:pk>/delete/', views.CountryDeleteView.as_view(), name='country_delete'),

    # Region URLs
    path('regions/', views.RegionListView.as_view(), name='region_list'),
    path('regions/<int:pk>/', views.RegionDetailView.as_view(), name='region_detail'),
    path('regions/create/', views.RegionCreateView.as_view(), name='region_create'),
    path('regions/<int:pk>/update/', views.RegionUpdateView.as_view(), name='region_update'),
    path('regions/<int:pk>/delete/', views.RegionDeleteView.as_view(), name='region_delete'),

    # City URLs
    path('cities/', views.CityListView.as_view(), name='city_list'),
    path('cities/<int:pk>/', views.CityDetailView.as_view(), name='city_detail'),
    path('cities/create/', views.CityCreateView.as_view(), name='city_create'),
    path('cities/<int:pk>/update/', views.CityUpdateView.as_view(), name='city_update'),
    path('cities/<int:pk>/delete/', views.CityDeleteView.as_view(), name='city_delete'),

    # District URLs
    path('districts/', views.DistrictListView.as_view(), name='district_list'),
    path('districts/<int:pk>/', views.DistrictDetailView.as_view(), name='district_detail'),
    path('districts/create/', views.DistrictCreateView.as_view(), name='district_create'),
    path('districts/<int:pk>/update/', views.DistrictUpdateView.as_view(), name='district_update'),
    path('districts/<int:pk>/delete/', views.DistrictDeleteView.as_view(), name='district_delete'),

    # Channel URLs
    path('channels/', views.ChannelListView.as_view(), name='channel_list'),
    path('channels/<int:pk>/', views.ChannelDetailView.as_view(), name='channel_detail'),
    path('channels/create/', views.ChannelCreateView.as_view(), name='channel_create'),
    path('channels/<int:pk>/update/', views.ChannelUpdateView.as_view(), name='channel_update'),
    path('channels/<int:pk>/delete/', views.ChannelDeleteView.as_view(), name='channel_delete'),

    # Outlet URLs
    path('outlets/', views.OutletListView.as_view(), name='outlet_list'),
    path('outlets/<int:pk>/', views.OutletDetailView.as_view(), name='outlet_detail'),
    path('outlets/create/', views.OutletCreateView.as_view(), name='outlet_create'),
    path('outlets/quick-add/', views.OutletQuickAddView.as_view(), name='outlet_quick_add'),
    path('outlets/<int:pk>/update/', views.OutletUpdateView.as_view(), name='outlet_update'),
    path('outlets/<int:pk>/delete/', views.OutletDeleteView.as_view(), name='outlet_delete'),

    # Data Loading URLs
    path('load-uzbekistan/', views.load_uzbekistan_data, name='load_uzbekistan'),
]
