from django.urls import path
from .views import dashboard_view, support_view, users_list_view, users_detail_view, foods_list_view, foods_detail_view, \
    categories_list_view, categories_detail_view, settings_view, settings_theme_view

app_name = 'crm'

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/users/', users_list_view, name='users_list'),
    path('dashboard/users/<int:pk>/', users_detail_view, name='users_detail'),
    path('dashboard/foods/', foods_list_view, name='foods_list'),
    path('dashboard/foods/<int:pk>/', foods_detail_view, name='foods_detail'),
    path('dashboard/categories/', categories_list_view, name='categories_list'),
    path('dashboard/categories/<int:pk>/', categories_detail_view, name='categories_detail'),
    path('dashboard/settings/', settings_view, name='dashboard_settings'),
    path('dashboard/settings/theme/', settings_theme_view, name='dashboard_settings_theme'),
    path('dashboard/support/<int:pk>/', support_view, name='dashboard_support')
]
