from django.apps import AppConfig


class CotisationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cotisations'

    def ready(self):
        import cotisations.signals
