from django.urls import path
from .views import home
from .api import FoodDetail, FoodList, CategoryList

app_name = 'main'

urlpatterns = [
    path("", home, name="home"),
    path("api/food-detail/<int:id>/", FoodDetail.as_view(), name="food_detail"),
    path("api/food-list/", FoodList.as_view(), name="food_list"),
    path("api/category-list/", CategoryList.as_view(), name="category_list"),
]
