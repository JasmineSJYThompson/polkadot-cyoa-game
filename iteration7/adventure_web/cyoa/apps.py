from django.apps import AppConfig


class CyoaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cyoa'

    def ready(self):
        from .models import Game
        from django.db.utils import OperationalError, ProgrammingError

        try:
            Game.objects.get_or_create(
                title="gilgamesh.exe",
                defaults={
                    "description": "A cyberpunk retelling of the Epic of Gilgamesh.",
                    "start_scene": "start_city_edge",
                }
            )
        except (OperationalError, ProgrammingError):
            # DB might not be ready yet during initial migrate
            pass
