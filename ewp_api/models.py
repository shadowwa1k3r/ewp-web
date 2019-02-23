from django.db import models


class Council(models.Model):
    title = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.title
