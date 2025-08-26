from django.apps import AppConfig


class QuotesConfig(AppConfig):
    """Конфигурация приложения."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.quotes"
    verbose_name = "Цитаты"
