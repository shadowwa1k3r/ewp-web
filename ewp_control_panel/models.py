from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from ewp_api.models import FcmDevices
import requests
import json
import os
from ewpadmin import settings
from tinytag import TinyTag
from pylibshout2 import Shout, ShoutProtocol, ShoutFormat
import threading
from pdf2image import convert_from_path
from django.core.files.base import ContentFile


class ApiKey(models.Model):
    key = models.TextField()
    mail = models.TextField()

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'api_keys'


class PushNotification(models.Model):
    title = models.TextField()
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return self.title


@receiver(post_save, sender=PushNotification)
def send_push_notification(instance, created, **kwargs):
    if created:
        reg_ids = []
        for device in FcmDevices.objects.all():
            reg_ids.append(device.device_token)
        payload = {"data": {
            "title": instance.title,
            "body": instance.body,
            "url": "myurl"
        },
            "notification": {
            "title": instance.title,
            "body": instance.body,
            "sound": "default",
        },
            "android": {
            "ttl": "86400s",
            "sound": "default",
            "priority": "high"
            },
            "registration_ids": reg_ids
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=AAAAYhf6ZJg:APA91bF6GrCPCkSe1xdptT5XTtiruB8ZVOp4w_C8JJ6v59ZCgaGgdSXZN3X1ho0xnjT6MbnXJmZcfJRPn6QByVZP69sXM_G2E33jxz0Ln_8lcrkTcaUJoFUHcRZbEtLiiL1FIgeNdX0G'
        }
        r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(payload), headers=headers)
        print(r.content)


class StreamAudioCategory(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'stream_categories'

    def __str__(self):
        return self.title

    @property
    def audio_count(self):
        return self.streamaudio_set.all().count


@receiver(post_save, sender=StreamAudioCategory)
def play_pasue_stream(instance, **kwargs):
    if instance.status:
        t = StartStreamOnNewThread(name=instance.title, stream_name=instance.title, category_id=instance.id)
        # t.daemon = True
        t.start()


class StartStreamOnNewThread(threading.Thread):
    def __init__(self, stream_name, category_id, *args, **kwargs):
        self.category_id = category_id
        self.stream_name = stream_name
        super(StartStreamOnNewThread, self).__init__(*args, **kwargs)

    def run(self):
        start_stream(self.stream_name, self.category_id)


def start_stream(stream_name, category_id):
    print('Started at: '+stream_name.lower())
    shout = Shout(
        host='localhost',
        port=8010,
        username='source',
        password='hackme',
        mount=stream_name.lower(),
        protocol=ShoutProtocol.HTTP,
        format=ShoutFormat.MP3)
    shout.open()
    should_restart = True
    while should_restart:
        for audiostream in StreamAudioCategory.objects.filter(id=category_id)[0].streamaudio_set.all():
            with open(audiostream.audiofile.path, 'rb') as fp:
                while True:
                    chunk = fp.read(1024)
                    if not chunk:
                        print('Next track at: '+stream_name.lower())
                        break
                    # print(StreamAudioCategory.objects.filter(id=category_id)[0].status)
                    if not StreamAudioCategory.objects.filter(id=category_id)[0].status:
                        print('Stopped by db at: '+stream_name.lower())
                        shout.close
                        return False
                    shout.send(chunk, 1024)
                    shout.sync()
        should_restart = True
    print('Stopped at: '+stream_name.lower())


class StreamAudio(models.Model):
    audiofile = models.FileField()
    title = models.CharField(max_length=255, blank=True)
    group = models.ForeignKey(StreamAudioCategory, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    duration = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'stream_audios'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.audiofile.name = os.path.basename(self.audiofile.name)
        return super(StreamAudio, self).save(*args, **kwargs)


@receiver(post_save, sender=StreamAudio)
def get_duration(instance, created, **kwargs):
    if created:
        tag = TinyTag.get(instance.audiofile.path)
        # print(str(int(tag.duration / 60)) + ':' + str(int(tag.duration % 60)))
        instance.duration = str(int(tag.duration / 60)) + ':' + str(int(tag.duration % 60))
        instance.title = str(instance.audiofile.name)
        instance.save()


class Book(models.Model):
    bookfile = models.FileField()
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    cover = models.ImageField(blank=True)

    class Meta:
        db_table = 'pdfbooks'

    def __str__(self):
        return self.title


@receiver(post_save, sender=Book)
def populate_data(instance, created, **kwargs):
    if created:
        page = convert_from_path(instance.bookfile.path, dpi=200, first_page=1, last_page=1)
        # print(settings.BASE_DIR+settings.MEDIA_URL+instance.title+'.jpg')
        page[0].save(settings.BASE_DIR+settings.MEDIA_URL+instance.title+'.jpg', 'JPEG')
        fh = open(settings.BASE_DIR+settings.MEDIA_URL+instance.title+'.jpg', 'rb')
        if fh:
            file_content = ContentFile(fh.read())
            instance.cover.save(instance.title+'.jpg', file_content)
