from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from stream.consumers import AdminConsumer


@receiver(post_save, sender=Order)
def assign_group_on_user_creation(sender, instance, created, **kwargs):
    if created:
        admin_consumer = AdminConsumer()
        AdminConsumer.send_order_list()
