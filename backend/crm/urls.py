from django.urls import path
from .views import dashboard_view, support_view, users_list_view, users_detail_view, foods_list_view, foods_detail_view, \
    categories_list_view, categories_detail_view, settings_view, settings_theme_view, food_delete_view, \
    category_delete_view, tips_list_view, tips_detail_view, tips_delete_view, extras_list_view, extras_delete_view, \
    extras_detail_view, orders_list_view, orders_detail_view, orders_create_view, orders_update_view

app_name = 'crm'

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/users/', users_list_view, name='users_list'),
    path('dashboard/users/<int:pk>/', users_detail_view, name='users_detail'),
    path('dashboard/orders/', orders_list_view, name='orders_list'),
    path('dashboard/orders/create/', orders_create_view, name='orders_create'),
    path('dashboard/orders/<int:pk>/update/', orders_update_view, name='orders_update'),
    path('dashboard/orders/<int:pk>/', orders_detail_view, name='orders_detail'),
    path('dashboard/foods/', foods_list_view, name='foods_list'),
    path('dashboard/foods/<int:pk>/', foods_detail_view, name='foods_detail'),
    path('dashboard/foods/delete/', food_delete_view, name='foods_delete'),
    path('dashboard/categories/', categories_list_view, name='categories_list'),
    path('dashboard/categories/<int:pk>/', categories_detail_view, name='categories_detail'),
    path('dashboard/categories/delete/', category_delete_view, name='categories_delete'),
    path('dashboard/tips/', tips_list_view, name='tips_list'),
    path('dashboard/tips/<int:pk>/', tips_detail_view, name='tips_detail'),
    path('dashboard/tips/delete/', tips_delete_view, name='tips_delete'),
    path('dashboard/extras/', extras_list_view, name='extras_list'),
    path('dashboard/extras/<int:pk>/', extras_detail_view, name='extras_detail'),
    path('dashboard/extras/delete/', extras_delete_view, name='extras_delete'),
    path('dashboard/settings/', settings_view, name='dashboard_settings'),
    path('dashboard/settings/theme/', settings_theme_view, name='dashboard_settings_theme'),
    path('dashboard/support/<int:pk>/', support_view, name='dashboard_support')
]
