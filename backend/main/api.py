from rest_framework.generics import RetrieveAPIView
from .serializers import FoodSerializer
from .models import Food


class FoodDetail(RetrieveAPIView):
    queryset = Food.objects.filter(is_active=True)
    serializer_class = FoodSerializer
    lookup_field = 'id'
