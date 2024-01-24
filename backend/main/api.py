from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import FoodSerializer, CategorySerializer
from .models import Food, Category


class FoodDetail(RetrieveAPIView):
    queryset = Food.objects.filter(is_active=True)
    serializer_class = FoodSerializer
    lookup_field = 'id'


class FoodList(ListAPIView):
    queryset = Food.objects.filter(is_active=True)
    serializer_class = FoodSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug']


class CategoryList(ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
