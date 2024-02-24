from django.db import models
from django.db.models import Sum, F
from main.models import Food
from django.contrib.auth import get_user_model
from account.models import Seat
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.shortcuts import reverse
from settings.models import Setting

# Create your models here.


class Extra(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Extra Name"))
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Extra Price"))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Visibility"),
        help_text=_("format: true=visible, false=hidden")
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"), blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"), blank=True, null=True)

    class Meta:
        verbose_name = _("Extra")
        verbose_name_plural = _("Extras")

    def __str__(self):
        return f"{self.name} - ${self.price}"

    def get_absolute_url(self):
        return reverse("crm:extras_detail", kwargs={"pk": self.pk})


class Tip(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Tip Name"))
    amount = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Tip Amount"))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Visibility"),
        help_text=_("format: true=visible, false=hidden")
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"), blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"), blank=True, null=True)

    class Meta:
        verbose_name = _("Tip")
        verbose_name_plural = _("Tips")

    def __str__(self):
        return f"{self.name} - ${self.amount}"

    def get_absolute_url(self):
        return reverse("crm:tips_detail", kwargs={"pk": self.id})


class Cart(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name=_("User"),
        related_name="cart_user",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text=_("The user who owns the cart.")
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Update"))

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        ordering = ("user",)

    def __str__(self):
        return self.user.get_name()

    def get_items(self):
        items = self.cart_items.all()
        items.filter(food__is_active=False).delete()
        return items

    def get_total_price(self):
        items = self.get_items()
        total_price = 0
        for item in items:
            total_price += item.food.price

        return total_price


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        verbose_name=_("Cart"),
        on_delete=models.CASCADE,
        related_name="cart_items",
        null=False,
        blank=False,
        help_text=_("The cart this item belongs to.")
    )
    food = models.ForeignKey(
        Food,
        verbose_name=_("Food"),
        on_delete=models.CASCADE,
        related_name="cart_item_food",
        null=False,
        blank=False,
        help_text=_("The food this item belongs to.")
    )
    seats = models.ManyToManyField(
        Seat,
        verbose_name=_("Seat"),
        related_name="cart_item_seats",
        blank=False,
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"), help_text=_("The quantity this item"))

    class Meta:
        verbose_name = _("CartItem")
        verbose_name_plural = _("CartItems")
        ordering = ["cart", "-id", "-quantity"]
        unique_together = ("cart", "food")

    def __str__(self):
        return f"{self.quantity} of {self.food}"


class Order(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        COMPLETED = "COMPLETED", _("Completed")

    class OrderStatusChoices(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PROCESSING = "PROCESSING", _("Processing")
        COMPLETED = "COMPLETED", _("Completed")

    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("User"),
        on_delete=models.PROTECT,
        related_name="orders",
        blank=False,
        null=False,
        help_text=_("The user who placed the order.")
    )
    session_id = models.UUIDField(
        verbose_name=_("Session ID"),
        blank=True,
        null=True,
        help_text=_("The session id of the order")
    )
    session_customer = models.CharField(
        verbose_name=_("Session Customer"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The session customer of the order")
    )
    extras = models.ManyToManyField(
        Extra,
        verbose_name=_("Extras"),
        blank=True,
        help_text=_("Selected extras for the order.")
    )
    tips = models.ForeignKey(
        Tip,
        verbose_name=_("Tips"),
        blank=True,
        null=True,
        help_text=_("Selected tips for the order."),
        on_delete=models.PROTECT
    )
    payment_method = models.CharField(
        max_length=50,
        verbose_name=_("Payment Method"),
        choices=Setting.PaymentGatewayChoices,
        default=Setting.PaymentGatewayChoices.CASH
    )
    payment_status = models.CharField(
        max_length=50,
        verbose_name=_("Payment Status"),
        choices=PaymentStatusChoices,
        default=PaymentStatusChoices.PENDING
    )
    status = models.CharField(
        max_length=50,
        verbose_name=_("Order Status"),
        choices=OrderStatusChoices,
        default=OrderStatusChoices.PENDING
    )
    description = models.TextField(
        verbose_name=_("Order Description"),
        blank=True,
        null=True,
        help_text=_("Additional notes or description for the order.")
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Order Date"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Modified"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ("-create_at",)

    def __str__(self):
        return f"Order #{self.id} - {self.user.get_name()}"

    def get_total_price(self):
        tip_amount = self.tips.amount if self.tips else 0
        extras_price = self.extras.aggregate(total=Sum("price"))["total"] or 0
        subtotal = self.get_subtotal()
        total_price = tip_amount + extras_price + subtotal
        return total_price

    def get_subtotal(self):
        return self.order_items.values("price", "quantity").aggregate(subtotal=Sum(F("price") * F("quantity")))[
            "subtotal"] or 0

    def get_extras_cost(self):
        return self.extras.values("price").aggregate(total=Sum("price"))["total"] or 0

    def get_absolute_url(self):
        return reverse("crm:orders_detail", kwargs={"pk": self.id})


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Order"),
        related_name="order_items",
        help_text=_("Order items are ordered by this order. ")
    )
    food = models.ForeignKey(
        Food,
        verbose_name=_("Food"),
        on_delete=models.CASCADE,
        related_name="order_item_food",
        null=False,
        blank=False,
        help_text=_("The food this item belongs to.")
    )
    seats = models.ManyToManyField(
        Seat,
        verbose_name=_("Seat"),
        related_name="order_item_seats",
        blank=False,
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"), help_text=_("The quantity this item"))
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Price"),
        null=True,
        blank=True,
        help_text=_("Cost of the food"),
    )

    class Meta:
        verbose_name = _("OrderItem")
        verbose_name_plural = _("OrderItems")
        ordering = ["order", "-id", "-quantity"]

    def __str__(self):
        return f"{self.quantity} of {self.food}"

    def total_cost(self):
        return self.price * self.quantity
