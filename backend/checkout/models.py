from django.db import models
from main.models import Food
from django.contrib.auth import get_user_model
from account.models import Seat
from django.utils.translation import gettext_lazy as _


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
        return self.name


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
