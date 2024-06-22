from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Client(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)  # otherwise error when clicking on tabs

    def __str__(self):
        return self.email


class Message(models.Model):
    subject = models.CharField(max_length=100)
    body = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)  # otherwise error when clicking on tabs

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('running', 'Running'),
        ('completed', 'Completed'),
    ]

    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    start_time = models.DateTimeField()
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.OneToOneField(Message,
                                   on_delete=models.CASCADE)  # Each Mailing can be associated with only one Message,
    # if the Message is deleted, the associated Mailing is also deleted.
    clients = models.ManyToManyField(
        Client)  # Each Mailing can be sent to multiple clients, and each client can receive multiple mailings
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # For managers to deactivate mailings

    def __str__(self):
        return f'Mailing {self.id} {self.status} {self.start_time}'


class Attempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)  # If the Mailing is deleted,
    # the associated Attempt is also deleted.
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)  # successful or not
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Attempt {self.id} for Mailing {self.mailing.id};\nStatus{self.status} {self.timestamp}'
