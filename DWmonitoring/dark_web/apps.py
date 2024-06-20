from django.apps import AppConfig


class DarkWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dark_web'

    def ready(self):
            import dark_web.signals