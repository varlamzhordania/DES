from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import Seat
from checkout.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = "__all__"

    def get_name(self, obj):
        return obj.get_alias_name()


class UserSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True, source='get_seats')
    customer_name = serializers.SerializerMethodField(source='get_name')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'customer_name', 'is_online', 'groups', 'seats')

    def get_customer_name(self, obj):
        return obj.get_name()
