from rest_framework import serializers
from .models import Cart, CartItem, Extra, Tip, Order
from main.serializers import FoodSerializer


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    payment_method = serializers.CharField(source='get_payment_method_display')
    payment_status = serializers.CharField(source='get_payment_status_display')
    total_price = serializers.SerializerMethodField(method_name='get_final_price')

    class Meta:
        model = Order
        fields = '__all__'

    def get_final_price(self, obj):
        return obj.get_total_price()


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


class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = '__all__'


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = '__all__'
