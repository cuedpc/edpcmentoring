from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AutonagConfig(AppConfig):
    name = 'autonag'
    verbose_name = 'User notification and reminding'

    def ready(self):
        # import signal handlers
        import autonag.signalhandlers as handlers

        # register notification creation handler
        post_migrate.connect(handlers.create_notice_types, sender=self)
