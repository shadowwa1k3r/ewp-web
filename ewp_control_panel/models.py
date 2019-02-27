from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin import messaging
import datetime


class ApiKey(models.Model):
    key = models.TextField()

    def __str__(self):
        return self.key


class PushNotification(models.Model):
    title = models.TextField()
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=PushNotification)
def send_push_notification(instance, created, **kwargs):
    if created:
        message = messaging.Message(
            notification=messaging.Notification(
                title=instance.title,
                body=instance.body,
            ),
            android=messaging.AndroidConfig(
                ttl=datetime.timedelta(seconds=3600),
                priority='normal',
                notification=messaging.AndroidNotification(
                    icon='stock_ticker_update',
                    color='#f45342'
                ),
            ),
            topic='ewp',
        )
        print(messaging.send(message))