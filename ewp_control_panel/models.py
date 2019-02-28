from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import json


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
        payload = {"data": {
            "title": instance.title,
            "body": instance.body,
            "url": "myurl"
        },
            "notification": {
            "title": instance.title,
            "body": instance.body,
        },
            "android": {
            "ttl": "86400s",
            "priority": "high"
            },
            "to": "/topics/ewp"
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=AAAAYhf6ZJg:APA91bF6GrCPCkSe1xdptT5XTtiruB8ZVOp4w_C8JJ6v59ZCgaGgdSXZN3X1ho0xnjT6MbnXJmZcfJRPn6QByVZP69sXM_G2E33jxz0Ln_8lcrkTcaUJoFUHcRZbEtLiiL1FIgeNdX0G'
        }
        r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(payload), headers=headers)
        print(r.content)
