from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from multiselectfield import MultiSelectField
from .validators import image_validator


class CustomMultiSelectField(MultiSelectField):
    def _get_flatchoices(self):
        flat_choices = super(models.CharField, self).flatchoices

        class MSFFlatchoices(list):
            # Used to trick django.contrib.admin.utils.display_for_field into not treating the list of values as a
            # dictionary key (which errors out)
            def __bool__(self):
                return False

            __nonzero__ = __bool__

        return MSFFlatchoices(flat_choices)

    flatchoices = property(_get_flatchoices)


def upload_logo(instance, filename):
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    extension = filename.split('.')[-1]
    return f'images/site/{timestamp}.{extension}'


class PaymentGateway(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Payment Gateway Name'))
    secret_key = models.CharField(max_length=255, verbose_name=_('Secret Key'), blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Create'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Date Update'))

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Setting(models.Model):
    class PaymentGatewayChoices(models.TextChoices):
        CASH = 'CASH', _('Cash')
        CREDIT = 'CREDIT', _('Credit')
        DEBIT = 'DEBIT', _('Debit')
        STRIPE = 'STRIPE', _('Stripe')

    company_name = models.CharField(
        max_length=255,
        verbose_name=_('Company Name'),
        blank=False,
        null=False,
        help_text=_("Company Name will be displayed on the home")
    )
    logo = models.FileField(
        upload_to=upload_logo,
        verbose_name=_('Logo'),
        help_text=_("it will be displayed for places that have big space"),
        validators=[image_validator],
        blank=True,
        null=True
    )
    logo_mini = models.FileField(
        upload_to=upload_logo,
        verbose_name=_('Logo mini'),
        help_text=_("small size of logo, for sidebar"),
        validators=[image_validator],
        blank=True,
        null=True
    )
    payment_gateways = CustomMultiSelectField(
        max_length=255,
        verbose_name=_('Payment Gateways'),
        blank=True,
        null=True,
        choices=PaymentGatewayChoices,
        help_text=_("Select one or more payment gateways")
    )
    payment_gateway_details = models.ManyToManyField(
        PaymentGateway,
        verbose_name=_("Payment Details"),
        related_name="setting_payment_detail",
        blank=True
    )

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")
        ordering = ("-id",)

    def __str__(self):
        return f"{self.id} - {self.company_name}"


class Theme(models.Model):
    name = models.CharField(
        verbose_name=_("Theme Name"),
        max_length=255,
        blank=False,
        null=False,
        unique=True,
        help_text=_("format: max-255, required")
    )
    primary_color = models.CharField(
        max_length=7,
        verbose_name=_("Primary Color"),
        blank=False,
        null=False,
        help_text=_("format: max-7, required example: #ff6e00")
    )
    secondary_color = models.CharField(
        max_length=7,
        verbose_name=_("Secondary Color"),
        blank=False,
        null=False,
        help_text=_("format: max-7, required example: #a088ef")
    )
    success_color = models.CharField(
        max_length=7,
        verbose_name=_("Success Color"),
        blank=False,
        null=False,
        help_text=_("format: max-7, required example: #4CAF50")
    )
    info_color = models.CharField(
        max_length=7,
        verbose_name=_("Information Color"),
        blank=False,
        null=False,
        help_text=_("format: max-7, required example: #2196F3")
    )
    warning_color = models.CharField(
        max_length=7,
        verbose_name=_("Warning Color"),
        blank=False,
        null=False,
        help_text=_("format: max-7, required example: #FFC107")
    )
    danger_color = models.CharField(
        max_length=7,
        verbose_name=_("Danger Color"),
        blank=False,
        null=False,
        help_text=_("format: max-7, required example: #D7385E")
    )
    light_color = models.CharField(
        max_length=7,
        verbose_name=_("Light Color"),
        blank=False,
        null=False,
        help_text=_("format: max-7, required example: #F8F9FA")
    )
    dark_color = models.CharField(
        max_length=7,
        verbose_name=_("Dark Color"),
        blank=False,
        null=False,
        help_text=_("format: max-7, required example: #2E384D")
    )
    body_bg_color = models.CharField(
        max_length=7,
        verbose_name=_("Background Color"),
        blank=False,
        null=False,
        help_text=_("format: max-7, required example: #f5f5f5")
    )
    is_primary = models.BooleanField(
        verbose_name=_("Primary Theme"),
        default=False,
        help_text=_("If primary it will be loaded")
    )

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")
        ordering = ["-is_primary", "id"]

    def __str__(self):
        return f"{self.id} - {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .theme import update_theme
        update_theme(self)
