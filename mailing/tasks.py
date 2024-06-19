from datetime import datetime

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail

from .models import Mailing, Attempt


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(start_time__lte=current_datetime, status='created')  # querying the database
    # for all Mailing objects whose start_time is less than or equal to the current time and whose status is 'created'.
    # This is done to get all the mailings that are scheduled to start now or in the past and have not been sent yet.

    for mailing in mailings:  # iterates over all mailings
        for client in mailing.clients.all():  # iterates over all clients in the mailing
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email]
                )
                Attempt.objects.create(mailing=mailing, status=True, response='success')  # creates an Attempt object
                # with status True and response 'success'
            except Exception as e:
                Attempt.objects.create(mailing=mailing, status=False, response=str(e))  # Attempt object with error msg
        mailing.status = 'completed'
        mailing.save()


def start():  # start a background scheduler that runs the send_mailing function every minute
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, trigger='interval',
                      minutes=1)  # Can be changed to cron
    scheduler.start()
