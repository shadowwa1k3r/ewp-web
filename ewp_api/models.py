from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import requests
from random import randint


class FcmDevices(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255)
    device_token = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'devices'

    def __str__(self):
        return self.device_id


class EwpUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    confirm_code = models.CharField(max_length=5)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'

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


class ChatRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rooms'

    def __str__(self):
        return self.name


@receiver(post_save, sender=EwpUser)
def create_user_room(instance, created, **kwargs):
    if created:
        ChatRoom.objects.create(user=instance.user, name=instance.user.username)


class Message(models.Model):
    body = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return self.body


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    message = models.TextField()
    created = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'feedbacks'

    def __str__(self):
        return self.title


class Aviarace(models.Model):
    code = models.IntegerField()
    city = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    geolocation = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'aviaraces'

    def __str__(self):
        return self.city


class Img(models.Model):
    imgurl = models.CharField(max_length=255, default="", blank=True)

    class Meta:
        db_table = 'images'

    def __str__(self):
        return self.imgurl


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

    class Meta:
        db_table = 'apartments'

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


class AlternativeNumber(models.Model):
    number = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'alternative_numbers'

    def __str__(self):
        return self.number


class WorkDay(models.Model):
    day = models.CharField(max_length=255, default='')
    time = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'work_days'

    def __str__(self):
        return self.day


class Council(models.Model):
    country = models.CharField(max_length=255, default='', blank=True)
    title = models.CharField(max_length=255, default='', blank=True)
    image_url = models.CharField(max_length=255, default='', blank=True)
    wikipedia_link = models.CharField(max_length=255, default='', blank=True)
    address = models.CharField(max_length=255, default='', blank=True)
    address_geo = models.CharField(max_length=255, default='', blank=True)
    site = models.CharField(max_length=255, default='', blank=True)
    email = models.CharField(max_length=255, default='', blank=True)
    number = models.CharField(max_length=255, default='', blank=True)
    alternative_numbers = models.ManyToManyField(AlternativeNumber, blank=True, related_name="alter_numbers")
    work_day = models.ManyToManyField(WorkDay, blank=True, related_name="work_day")

    class Meta:
        db_table = 'councils'
        ordering = ['-id', ]

    def __str__(self):
        return self.title

    @property
    def phone_numbers(self):
        """
        :return: alternative numbers in html format
        """
        if self.alternative_numbers.count() > 1:
            numbers = ''
            for num in self.alternative_numbers.all():
                numbers += f"{num.number} <br>"
            return numbers
        elif self.alternative_numbers.count() == 1:
            return self.alternative_numbers.first()
        else:
            return ''

    @property
    def working_days(self):
        """
        :return: working days in html format
        """
        if self.work_day.count() > 1:
            days = ''
            for day in self.work_day.all():
                days += f"{day.day} <br>"
            return days
        elif self.work_day.count() == 1:
            return self.work_day.first()
        else:
            return ''


@receiver(pre_delete, sender=Council)
def delete_numbers_and_days(instance, **kwargs):
    instance.work_day.all().delete()
    instance.alternative_numbers.all().delete()
