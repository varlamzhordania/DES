# management/commands/deactivate_rooms.py
from django.core.management.base import BaseCommand
from stream.models import UserRoom


class Command(BaseCommand):
    help = 'Deactivate all rooms on server start'

    def handle(self, *args, **options):
        UserRoom.objects.all().update(is_active=False)
        self.stdout.write(self.style.SUCCESS('All rooms deactivated successfully.'))
