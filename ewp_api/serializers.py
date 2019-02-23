from rest_framework import serializers
from .models import Council


class CouncilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Council
        fields = ("title",)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
