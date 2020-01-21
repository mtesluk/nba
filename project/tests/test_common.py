from rest_framework.test import APIClient, APITestCase
from account.models import *
from django.contrib.auth.models import User
from nba.models import *


class PlayersTests(APITestCase):
    def setUp(self):
        client = APIClient()
        Season.objects.create(name='2017-18')
        self.username = 'user1'
        self.password = 'pass1'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)

    def test_get_seasons(self):
        response = self.client.get('/api/v1/seasons/')
        data = response.json()
        results = data['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], '2017-18')
