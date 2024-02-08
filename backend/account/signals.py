from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(post_save, sender=get_user_model())
def assign_group_on_user_creation(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            manager_group, created = Group.objects.get_or_create(name='Manager')
            instance.groups.add(manager_group)
        else:
            table_group, created = Group.objects.get_or_create(name='Table')
            instance.groups.add(table_group)
