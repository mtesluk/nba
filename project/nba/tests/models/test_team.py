from django.test import TestCase
from nba.models import Team


class TeamTestCase(TestCase):
    def setUp(self):
        self.name = 'Golden State Warriors'

    def test_team(self):
        team_obj = Team.objects.create(name=self.name)
        self.assertEqual(team_obj.name, self.name)
