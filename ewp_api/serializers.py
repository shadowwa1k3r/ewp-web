from rest_framework.serializers import ModelSerializer, Serializer, CharField
from .models import Council, Aviarace, Img, Apartment, AlternativeNumber, WorkDay
from ewp_control_panel.models import Book, StreamAudioCategory


class WorkDaySerializer(ModelSerializer):
    class Meta:
        model = WorkDay
        fields = [
            'day',
            'time'
        ]


class AlternativeNumberSerializer(ModelSerializer):
    class Meta:
        model = AlternativeNumber
        fields = [
            'number'
        ]


class CouncilSerializer(ModelSerializer):
    alternative_numbers = AlternativeNumberSerializer(many=True)
    work_day = WorkDaySerializer(many=True)

    class Meta:
        model = Council
        fields = [
            'country',
            'title',
            'image_url',
            'wikipedia_link',
            'address',
            'address_geo',
            'site',
            'email',
            'number',
            'alternative_numbers',
            'work_day'
        ]


class StreamListSerializer(ModelSerializer):
    class Meta:
        model = StreamAudioCategory
        fields = [
            'title'
        ]


class BookListSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'bookfile',
            'title',
            'created',
            'cover',
        ]


class TokenSerializer(Serializer):
    token = CharField(max_length=255)


class AviaraceListSerializer(ModelSerializer):
    class Meta:
        model = Aviarace
        fields = [
            'code',
            'city',
            'address',
            'geolocation',
        ]


class ImgListSerializer(ModelSerializer):
    class Meta:
        model = Img
        fields = [
            'id',
            'imgurl'
        ]


class ApartmentListSerializer(ModelSerializer):
    images = ImgListSerializer(many=True)

    class Meta:
        model = Apartment
        fields = [
            'id',
            'avitoid',
            'lat',
            'lng',
            'city',
            'person_type',
            'source',
            'metro',
            'url',
            'cat1_id',
            'description',
            'nedvigimost_type',
            'price',
            'cat_2',
            'contactname',
            'cat_1',
            'apartment_id',
            'person',
            'address',
            'cat2_id',
            'time',
            'title',
            'phone',
            'person_type_id',
            'nedvigimost_type_id',
            'source_id',
            'region',
            'city_1',
            'phone_operator',
            'images',
            'params',

        ]
