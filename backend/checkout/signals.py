from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction


@receiver(post_save, sender=Order)
def send_order_list_signal(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    transaction.on_commit(
        lambda: async_to_sync(channel_layer.group_send)('admin_room', {'type': 'send.order_list', 'dict_data': {}})
        )
