from rest_framework.test import APIClient, APITestCase
from account.models import *
from django.contrib.auth.models import User


class PlayersTests(APITestCase):
    def setUp(self):
        client = APIClient()
        self.username = 'user1'
        self.password = 'pass1'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)

    def test_get_seasons(self):
        pass

    def test_get_season_files(self):
        pass