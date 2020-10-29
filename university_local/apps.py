from django.apps import AppConfig


class UniversitiesConfig(AppConfig):
    name = 'university_local'

    def ready(self):
        import university_local.signals

