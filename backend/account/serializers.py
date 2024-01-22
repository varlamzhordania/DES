from rest_framework import serializers
from .models import User, Seat


class SeatSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = "__all__"

    def get_name(self, obj):
        return obj.get_alias_name()


class UserSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True, source='get_seats')

    class Meta:
        model = User
        exclude = ["password", "user_permissions", "groups"]
