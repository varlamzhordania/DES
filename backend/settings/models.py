from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


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
