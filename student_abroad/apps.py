from django.apps import AppConfig


class StudentsConfig(AppConfig):
    name = 'student_abroad'

    def ready(self):
        import student_abroad.signals

