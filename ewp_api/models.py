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
        r = requests.get('https://cdn.osg.uz/sms/?phone={}&id=4342&message={}'.format(phone, code))


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
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Aviarace(models.Model):
    code = models.IntegerField()
    city = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    geolocation = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.city


class Img(models.Model):
    imgurl = models.CharField(max_length=255, default="", blank=True)


class Apartment(models.Model):
    avitoid = models.IntegerField(default=0, blank=True)
    lat = models.CharField(max_length=255, default="", blank=True)
    lng = models.CharField(max_length=255, default="", blank=True)
    city = models.CharField(max_length=255, default="", blank=True)
    person_type = models.CharField(max_length=255, default="", blank=True)
    source = models.CharField(max_length=255, default="", blank=True)
    metro = models.CharField(max_length=255, default="", blank=True)
    url = models.CharField(max_length=255, default="", blank=True)
    cat1_id = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField(default="", blank=True)
    nedvigimost_type = models.CharField(max_length=255, default="", blank=True)
    price = models.CharField(max_length=255, default="", blank=True)
    cat_2 = models.CharField(max_length=255, default="", blank=True)
    contactname = models.CharField(max_length=255, default="", blank=True)
    cat_1 = models.CharField(max_length=255, default="", blank=True)
    apartment_id = models.CharField(max_length=255, default="", blank=True)
    person = models.CharField(max_length=255, default="", blank=True)
    address = models.CharField(max_length=255, default="", blank=True)
    cat2_id = models.CharField(max_length=255, default="", blank=True)
    time = models.CharField(max_length=255, default="", blank=True)
    title = models.CharField(max_length=255, default="", blank=True)
    phone = models.CharField(max_length=255, default="", blank=True)
    person_type_id = models.CharField(max_length=255, default="", blank=True)
    nedvigimost_type_id = models.CharField(max_length=255, default="", blank=True)
    source_id = models.CharField(max_length=255, default="", blank=True)
    region = models.CharField(max_length=255, default="", blank=True)
    city_1 = models.CharField(max_length=255, default="", blank=True)
    phone_operator = models.CharField(max_length=255, default="", blank=True)
    images = models.ManyToManyField(Img)
    params = models.TextField()

    def __str__(self):
        return self.title

    @staticmethod
    def save_as_object(json_dick):
        for data in json_dick['data']:
            apartment = Apartment(
                avitoid=data['avitoid'],
                lat=data['coords']['lat'],
                lng=data['coords']['lng'],
                city=data['city'],
                person_type=data['person_type'],
                source=data['source'],
                metro=data['metro'],
                url=data['url'],
                cat1_id=data['cat1_id'],
                description=data['description'],
                nedvigimost_type=data['nedvigimost_type'],
                price=data['price'],
                cat_2=data['cat2'],
                contactname=data['contactname'],
                cat_1=data['cat1'],
                apartment_id=data['id'],
                person=data['person'],
                address=data['address'],
                cat2_id=data['cat2_id'],
                time=data['time'],
                title=data['title'],
                phone=data['phone'],
                person_type_id=data['person_type_id'],
                nedvigimost_type_id=data['nedvigimost_type_id'],
                source_id=data['source_id'],
                region=data['region'],
                city_1=data['city1'],
                phone_operator=data['phone_operator'],
                params=data['params'],
            )
            apartment.save()
            for img in data['images']:
                image = Img(imgurl=img['imgurl'])
                image.save()
                apartment.images.add(image)
                apartment.save()
