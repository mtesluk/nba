from rest_framework.test import APIClient, APITestCase
from account.models import *
from django.contrib.auth.models import User
from nba.models import *


class PlayersTests(APITestCase):
    def setUp(self):
        client = APIClient()
        self.players_name = ['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'RR', 'GG', 'GH', 'FD', 'RT', 'RA']
        self.username = 'user1'
        self.password = 'pass1'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)

    def _prepare_data(self):
        s = Season.objects.create(name='2017-18')
        stat = Stat.objects.create(type='int', name='PTS')
        for i in range(len(self.players_name)):
            p = Player.objects.create(name=self.players_name[i], position='C', age='22')
            PlayerStat.objects.create(player=p, season=s, stat=stat, value=(i * 3))

    def test_get_players(self):
        self._prepare_data()

        params = {'season': '1', 'page': '1', 'page_size': 5}
        response = self.client.get('/api/v1/players/', params)
        data = response.json()
        results = data['results']

        self.assertEqual(len(results), 5)

        for result in results:
            self.assertIn(result['name'], self.players_name)
            self.assertTrue(result['stats'])
