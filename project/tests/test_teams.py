from rest_framework.test import APIClient, APITestCase, RequestsClient
from account.models import *
from django.contrib.auth.models import User
from nba.models import *


class TeamTests(APITestCase):
    def setUp(self):
        client = RequestsClient()
        self.teams_name = ['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'RR', 'GG', 'GH', 'FD', 'RT', 'RA']
        self.username = 'user1'
        self.password = 'pass1'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)

    def _prepare_data(self):
        s = Season.objects.create(name='2017-18')
        stat = Stat.objects.create(type='int', name='PTS')
        for i in range(len(self.teams_name)):
            t = Team.objects.create(name=self.teams_name[i])
            TeamStat.objects.create(team=t, season=s, stat=stat, value=(i * 3))

    def test_get_teams(self):
        self._prepare_data()

        params = {'season': '1', 'page': '1', 'page_size': 4}
        response = self.client.get('/api/v1/teams/', params)
        data = response.json()
        results = data['results']

        self.assertEqual(len(results), 4)

        for result in results:
            self.assertIn(result['name'], self.teams_name)
            self.assertTrue(result['stats'])

    def test_bet_teams(self):
        self.client.login(username=self.username, password=self.password)

        self.assertEqual(self.profile.credits, 100)
        self.client.post('/api/v1/teams/bet/')

        updated_credits = Profile.objects.get(user=User.objects.get(username=self.username)).credits
        self.assertEqual(updated_credits, 95)
