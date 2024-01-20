from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


def category_image(instance, filename):
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    extension = filename.split('.')[-1]
    return f'images/category/{timestamp}.{extension}'


def food_image(instance, filename):
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    extension = filename.split('.')[-1]
    return f'images/food/{timestamp}.{extension}'


class Category(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        help_text=_("format: max-255, required")
    )
    slug = AutoSlugField(
        populate_from="name",
        blank=True,
        null=True,
        help_text=_("format: automatically created")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True,
        help_text=_("Additional details about the category")
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to=category_image,
        null=True,
        blank=True,
        help_text=_("Category image")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Visibility"),
        help_text=_("format: true=visible, false=hidden")
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"), blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"), blank=True, null=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("-id",)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        help_text=_("format: max-255, required")
    )
    slug = AutoSlugField(
        populate_from="name",
        blank=True,
        null=True,
        help_text=_("format: automatically created")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True,
        help_text=_("Additional details about the food")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="food_category",
        verbose_name=_("Category"),
        help_text=_("Food Category")
    )
    thumbnail = models.ImageField(
        verbose_name=_("Image"),
        upload_to=food_image,
        null=True,
        blank=True,
        help_text=_("Food thumbnail image")
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Price"),
        null=True,
        blank=True,
        help_text=_("Cost of the food"),
        validators=[
            MinValueValidator(Decimal(0.00))
        ]
    )
    ingredients = models.TextField(
        verbose_name=_("Ingredients"),
        blank=True,
        null=True,
        help_text=_("List of ingredients used in the food")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Visibility"),
        help_text=_("format: true=visible, false=hidden")
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Create"), blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"), blank=True, null=True)

    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Foods")
        ordering = ("-id",)

    def __str__(self):
        return self.name
