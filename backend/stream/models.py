from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


# Create your models here.


class UserRoom(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name=_("User"),
        related_name="user_room",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    support = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Support"),
        related_name="user_support",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(verbose_name=_("Active"), default=False)
    is_busy = models.BooleanField(verbose_name=_("Busy"), default=False)
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta(object):
        verbose_name = _("User Room")
        verbose_name_plural = _("User Rooms")
        ordering = ("-is_active", "-update_at", "-is_busy")

    def __str__(self):
        return self.user.username
