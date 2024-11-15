from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from .serializers import FoodSerializer, CategorySerializer
from .models import Food, Category


class FoodDetail(RetrieveAPIView):
    queryset = Food.objects.filter(is_active=True)
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class FoodList(ListAPIView):
    queryset = Food.objects.filter(is_active=True)
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category__slug']
    search_fields = ['name']


class CategoryList(ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
