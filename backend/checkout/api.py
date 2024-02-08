from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .serializers import CartSerializer, CartItemSerializer, ExtraSerializer, TipSerializer, OrderSerializer
from .models import CartItem, Cart, Extra, Tip, Order
from main.models import Food
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from account.utils import get_current_session
import logging

logger = logging.getLogger(__name__)


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
                    seats = item.get('seats', [])
                    try:
                        food = Food.objects.get(pk=food_id, is_active=True)
                    except Food.DoesNotExist:
                        return Response(
                            {"error": "food is not available", "data": item},
                            status=status.HTTP_404_NOT_FOUND
                        )

                    cart_item_data = {'quantity': quantity}

                    cart_item, created = CartItem.objects.update_or_create(
                        cart=user_cart, food=food, defaults=cart_item_data
                    )

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


class OrderListView(APIView):
    pagination_class = PageNumberPagination
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        session = get_current_session(request)
        orders = Order.objects.filter(user=request.user, session_id=session.get("session_id", None)).order_by(
            "create_at"
        )

        # Paginate the queryset
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(orders, request)

        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ExtraView(ListAPIView):
    queryset = Extra.objects.filter(is_active=True)
    serializer_class = ExtraSerializer
    permission_classes = [permissions.IsAuthenticated]


class TipView(ListAPIView):
    queryset = Tip.objects.filter(is_active=True)
    serializer_class = TipSerializer
    permission_classes = [permissions.IsAuthenticated]
