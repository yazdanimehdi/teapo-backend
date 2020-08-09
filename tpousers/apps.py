from django.apps import AppConfig


class TpousersConfig(AppConfig):
    name = 'tpousers'

    def ready(self):
        import tpousers.signals
