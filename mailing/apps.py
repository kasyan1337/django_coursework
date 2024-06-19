from time import sleep

from django.apps import AppConfig

from mailing.tasks import start


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):  # added manually
        sleep(2)
        start()  # start the scheduler when the app is ready, custom function from tasks module
