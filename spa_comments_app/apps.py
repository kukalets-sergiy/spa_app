from django.apps import AppConfig


class SpaCommentsAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "spa_comments_app"


    def ready(self):
        import spa_comments_app.signals
