from django.db import models


class ApiKey(models.Model):
    key = models.TextField()

    def __str__(self):
        return self.key
