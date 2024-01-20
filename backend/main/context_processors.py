from django.conf import settings
from settings.models import Theme


def Default(request):
    return {
        "theme": Theme.objects.filter(is_primary=True).first()
    }
