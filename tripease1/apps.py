from django.apps import AppConfig


class Tripease1Config(AppConfig):
    name = 'tripease1'

    def ready(self):
        import tripease1.signals