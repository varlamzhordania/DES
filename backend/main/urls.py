from django.urls import path
from .views import home
from .api import FoodDetail

app_name = 'main'

urlpatterns = [
    path("", home, name="home"),
    path("api/food-detail/<int:id>/", FoodDetail.as_view(), name="food_detail")
]
