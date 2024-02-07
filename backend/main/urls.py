from django.urls import path
from .views import home_view, support_view, settings_view
from .api import FoodDetail, FoodList, CategoryList

app_name = 'main'

urlpatterns = [
    path("", home_view, name="home"),
    path("support/", support_view, name="support"),
    path("settings/", settings_view, name="settings"),
    path("api/food-detail/<int:id>/", FoodDetail.as_view(), name="food_detail"),
    path("api/food-list/", FoodList.as_view(), name="food_list"),
    path("api/category-list/", CategoryList.as_view(), name="category_list"),
]
