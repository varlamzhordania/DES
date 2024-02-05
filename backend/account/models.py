from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.


class User(AbstractUser):
    is_online = models.BooleanField(default=False, help_text="User status", verbose_name='Online')

    def __str__(self):
        return self.username

    def get_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.username

    def get_seats(self):
        return self.user_seat.all()


class Seat(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), related_name="user_seat", on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField(verbose_name=_("Seat Number"), default=0)
    seat_name = models.CharField(
        verbose_name=_("Seat Name"),
        max_length=255,
        help_text=_("example john doe seats on number 2, instead of calling the seat number 2 we call it john seat"),
        null=True,
        blank=True
    )
    is_available = models.BooleanField(verbose_name=_("Is available"), default=True)

    class Meta:
        verbose_name = _("Seat")
        verbose_name_plural = _("Seats")
        ordering = ['user', 'seat_number', '-is_available', 'seat_name']

    def __str__(self):
        return f"{self.user.get_name()}.{self.seat_number}"

    def get_alias_name(self):
        if self.seat_name:
            return self.seat_name
        else:
            return f"{self.user.get_name()}:{self.seat_number}"
