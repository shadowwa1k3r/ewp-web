from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from random import randint


class Council(models.Model):
    title = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.title


class EwpUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    confirm_code = models.CharField(max_length=5)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @staticmethod
    def generate_confirm_code():
        return str(randint(0, 9))+str(randint(0, 9))+str(randint(0, 9))+str(randint(0, 9))+str(randint(0, 9))

    @staticmethod
    def send_confirm_code(phone, code):
        print(code)
        r = requests.get('https://cdn.osg.uz/sms/?phone={}&id=4342&message={}'.format())


@receiver(post_save, sender=User)
def create_ewp_user(instance, created, **kwargs):
    if created:
        EwpUser.objects.create(user=instance)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    message = models.TextField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Aviarace(models.Model):
    code = models.CharField(max_length=25, default='')
    city = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    geolocation = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'aviarace'

    def __str__(self):
        return self.city
