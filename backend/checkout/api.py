from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CartSerializer, CartItemSerializer
from .models import CartItem, Cart
from main.models import Food
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


class CartView(APIView):

    def get(self, request):
        user_cart = Cart.objects.filter(user=request.user).first()
        serializer = CartSerializer(user_cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            user_cart, created = Cart.objects.get_or_create(user=request.user)
            data = request.data

            with transaction.atomic():
                new_list = []

                for item in data:
                    food_id = item.get('id')
                    quantity = item.get('quantity', 1)
                    extras = item.get('extras', [])
                    seats = item.get('seats', [])

                    food = get_object_or_404(Food, pk=food_id)

                    cart_item_data = {'quantity': quantity}

                    cart_item, created = CartItem.objects.update_or_create(
                        cart=user_cart, food=food, defaults=cart_item_data
                    )

                    cart_item.extras.set(extras)
                    cart_item.seats.set(seats)
                    new_list.append(cart_item.id)

                deleted_items = CartItem.objects.filter(
                    ~Q(id__in=new_list),
                    cart=user_cart
                )

                deleted_items.delete()

            return Response({"success": "cart items successfully updated"}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            logger.error("Cart or Food dose not exist : ", e)
            return Response({"error": "Cart or Food dose not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error("Ops!!! something went wrong when trying to update cart : ", e)
            return Response(
                {"error": "Ops!!! something went wrong when trying to update cart"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
