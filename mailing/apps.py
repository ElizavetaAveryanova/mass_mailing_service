from django.apps import AppConfig
import time


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        from scheduler import start
        time.sleep(2)
        start()
