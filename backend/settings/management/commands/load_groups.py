from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Load default groups'

    DEFAULT_GROUPS = ['Table', 'Manager']

    def handle(self, *args, **kwargs):
        try:
            for group_name in self.DEFAULT_GROUPS:
                group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Group "{group.name}" created successfully'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Group "{group.name}" already exists'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR('User terminated the load process'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred while trying to load the default groups:\n{e}'))
