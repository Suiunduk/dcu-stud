from django.apps import AppConfig


class UniversitiesConfig(AppConfig):
    name = 'universities'

    def ready(self):
        import universities.signals

