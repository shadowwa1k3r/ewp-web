from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from .models import Council
from .serializers import CouncilSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_council(title=''):
        if title != '':
            Council.objects.create(title=title)

    def setUp(self):
        self.create_council('loki')
        self.create_council('thor')
        self.create_council('ironman')
        self.create_council('captain america')


class GetAllCouncilTest(BaseViewTest):

    def test_get_all_council(self):
        response = self.client.get(reverse('council-all'))

        expected = Council.objects.all()
        serialized = CouncilSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, serialized.HTTP_200_OK)
