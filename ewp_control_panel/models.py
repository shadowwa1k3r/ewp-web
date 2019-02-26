from django.db import models


class ApiKey(models.Model):
    key = models.TextField()

    def __str__(self):
        return self.key


class PushNotification(models.Model):
    title = models.TextField()
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
