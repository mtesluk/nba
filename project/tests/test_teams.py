from rest_framework.test import APIClient, APITestCase, RequestsClient
from account.models import Profile
from django.contrib.auth.models import User
from nba.models import Stat, Season, Team, TeamStat


class TeamTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.teams_name = ['AA', 'CC', 'BB', 'DD', 'EE', 'FF', 'RR', 'GG', 'GH', 'FD', 'RT', 'RA']
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

        params = {'season': '1'}
        response = self.client.get('/api/v1/teams/', params)
        data = response.json()
        results = data['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 10)

        for result in results:
            self.assertIn(result['name'], self.teams_name)
            self.assertTrue(result['stats'])

    def test_get_paginated_teams(self):
        self._prepare_data()

        params = {'season': '1', 'page': '1', 'page_size': 4}
        response = self.client.get('/api/v1/teams/', params)
        data = response.json()
        results = data['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 4)

        for result in results:
            self.assertIn(result['name'], self.teams_name)
            self.assertTrue(result['stats'])

    def test_get_filtered_teams(self):
        self._prepare_data()

        params = {'season': '1', 'name': 'AA'}
        response = self.client.get('/api/v1/teams/', params)
        data = response.json()
        results = data['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 1)
        self.assertIn('AA', self.teams_name)

    def test_get_sorted_teams(self):
        self._prepare_data()
        sorted_names = sorted(self.teams_name)[:10]

        params = {'season': '1', 'ordering': 'name'}
        response = self.client.get('/api/v1/teams/', params)
        data = response.json()
        results = data['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 10)
        self.assertEqual(sorted_names, [result['name'] for result in results])

    def test_bet_teams(self):
        self.client.login(username=self.username, password=self.password)

        self.assertEqual(self.profile.credits, 100)
        response = self.client.post('/api/v1/teams/bet/')

        updated_credits = Profile.objects.get(user=User.objects.get(username=self.username)).credits
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_credits, 95)
