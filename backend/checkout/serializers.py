from rest_framework import serializers
from .models import Cart, CartItem
from main.serializers import FoodSerializer


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_cart_items(self, obj):
        items = obj.get_items()
        return CartItemSerializer(items, many=True).data


class CartItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'
