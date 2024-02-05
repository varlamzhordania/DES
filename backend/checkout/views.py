from django.shortcuts import render, redirect
from .models import Order, OrderItem, Extra, Tip
from core.utils import fancy_message
from django.db import transaction
from django.contrib.auth.decorators import login_required


def full_fill_order(request, user_cart, tips, extras, description, method):
    try:
        with transaction.atomic():
            session_id = request.session.get('session_id', '')
            session_customer = request.session.get('customer', '')
            order = Order.objects.create(
                user=request.user,
                tips=Tip.objects.get(pk=tips) if tips else None,
                payment_method=method,
                description=description,
                session_id=session_id,
                session_customer=session_customer
            )

            if extras:
                order.extras.set(Extra.objects.filter(pk__in=extras))

            for cart_item in user_cart:
                order_item = OrderItem.objects.create(
                    order=order,
                    food=cart_item.food,
                    quantity=cart_item.quantity,
                    price=cart_item.food.price * cart_item.quantity,
                )

                order_item.seats.set(cart_item.seats.all())

            user_cart.delete()

            return order.id

    except Exception as e:
        print(f"Error while processing order: {e}")
    return None


@login_required
def checkout(request, *args, **kwargs):
    if request.method == "POST":
        description = request.POST.get("description", None)
        extras = request.POST.getlist("extras", [])
        tips = request.POST.get("tips", None)
        payment_method = request.POST.get("payment", None)

        user_cart = request.user.cart_user.get_items()

        if payment_method == "cash":
            method = Order.PaymentMethodChoices.CASH
            order_id = full_fill_order(request, user_cart, tips, extras, description, method)
            if order_id:
                fancy_message(
                    request,
                    "Your order has been successfully submitted. After review, it will be processed. Thank you for choosing us!",
                    level="success"
                )
            else:
                fancy_message(request, "An error occurred while processing the order.", level="error")
        elif payment_method == "credit":
            pass
        else:
            fancy_message(
                request,
                "Payment method is invalid, please make sure you have selected correct method",
                level="error"
            )
    return redirect("main:home")
