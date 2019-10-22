from django.test import TestCase
from nba.models import Season


class SeasonTestCase(TestCase):
    def setUp(self):
        self.name = '2017-18'

    def test_season(self):
        season_obj = Season.objects.create(name=self.name)
        self.assertEqual(season_obj.name, self.name)
