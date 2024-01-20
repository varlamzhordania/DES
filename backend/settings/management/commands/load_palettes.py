from django.core.management.base import BaseCommand
from settings.models import Theme
from django.conf import settings


class Command(BaseCommand):
    help = 'Load default palettes'

    DEFAULT_PALETTES = [
        {
            'name': "green/blue theme",
            'primary_color': "#2ecc71",
            'secondary_color': "#3498db",
            'success_color': "#27ae60",
            'info_color': "#3498db",
            'warning_color': "#f39c12",
            'danger_color': "#e74c3c",
            'light_color': "#ecf0f1",
            'dark_color': "#34495e",
            'body_bg_color': "#ecf0f1",
            'is_primary': False,
        },
        {
            'name': "purple/red theme",
            'primary_color': "#9b59b6",
            'secondary_color': "#e74c3c",
            'success_color': "#2ecc71",
            'info_color': "#3498db",
            'warning_color': "#f39c12",
            'danger_color': "#e74c3c",
            'light_color': "#ecf0f1",
            'dark_color': "#34495e",
            'body_bg_color': "#ecf0f1",
            'is_primary': False,
        },
        {
            'name': "blue/orange theme",
            'primary_color': "#3498db",
            'secondary_color': "#e67e22",
            'success_color': "#27ae60",
            'info_color': "#9b59b6",
            'warning_color': "#f1c40f",
            'danger_color': "#c0392b",
            'light_color': "#ecf0f1",
            'dark_color': "#34495e",
            'body_bg_color': "#ecf0f1",
            'is_primary': False,
        },
        {
            'name': "teal/yellow theme",
            'primary_color': "#008080",
            'secondary_color': "#FFD700",
            'success_color': "#008000",
            'info_color': "#87CEEB",
            'warning_color': "#FFA500",
            'danger_color': "#FF0000",
            'light_color': "#F0FFF0",
            'dark_color': "#2F4F4F",
            'body_bg_color': "#F0FFF0",
            'is_primary': False,
        },
        {
            'name': "pink/green theme",
            'primary_color': "#FF69B4",
            'secondary_color': "#008000",
            'success_color': "#ADFF2F",
            'info_color': "#87CEEB",
            'warning_color': "#FFD700",
            'danger_color': "#FF0000",
            'light_color': "#FFF0F5",
            'dark_color': "#2F4F4F",
            'body_bg_color': "#FFF0F5",
            'is_primary': False,
        },
        {
            'name': "orange/purple theme",
            'primary_color': "#FFA500",
            'secondary_color': "#800080",
            'success_color': "#008000",
            'info_color': "#87CEEB",
            'warning_color': "#FFD700",
            'danger_color': "#FF0000",
            'light_color': "#FFFAF0",
            'dark_color': "#2F4F4F",
            'body_bg_color': "#FFFAF0",
            'is_primary': False,
        },
        {
            'name': "blue/red theme",
            'primary_color': "#0000FF",
            'secondary_color': "#FF0000",
            'success_color': "#008000",
            'info_color': "#87CEEB",
            'warning_color': "#FFD700",
            'danger_color': "#FF0000",
            'light_color': "#F0F8FF",
            'dark_color': "#2F4F4F",
            'body_bg_color': "#F0F8FF",
            'is_primary': False,
        },
    ]

    def handle(self, *args, **kwargs):
        try:
            for palette_data in self.DEFAULT_PALETTES:
                theme, created = Theme.objects.update_or_create(name=palette_data['name'], defaults=palette_data)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Theme palette "{theme.name}" created successfully'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Theme palette "{theme.name}" updated successfully'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR('User terminated the load process'))
        except Exception as e:
            self.stdout.write(self.style.ERROR("An error occurred while trying to load the theme palettes, ", e))
