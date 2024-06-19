from time import sleep

from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):  # added manually
        from mailing.tasks import start  # This had to be moved here instead of being on the top of the file,
        # otherwise it would load before the app is ready and I would get:
        # 'django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.'
        sleep(2)
        start()  # start the scheduler when the app is ready, custom function from tasks module
