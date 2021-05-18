from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Class defining app configurations.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.authentication'
