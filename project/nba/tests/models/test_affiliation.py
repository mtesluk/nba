from django.test import TestCase
from nba.models import Player, Season, Affiliation


class AffiliationTestCase(TestCase):
    def setUp(self):
        self.season = '2017-18'
        self.name = 'LeBron James'
        self.age = 34
        self.position = 'SF'
        self.teams = ['Cleveland Cavaliers', 'Los Angeles Lakers']

    def test_player(self):
        player_obj = Player.objects.create(name=self.name, age=self.age, position=self.position)
        season_obj = Season.objects.create(name=self.season)
        affiliation_obj = Affiliation.objects.create(season=season_obj, player=player_obj)
        team1_obj = affiliation_obj.teams.create(name=self.teams[0])
        team2_obj = affiliation_obj.teams.create(name=self.teams[1])

        self.assertEqual(affiliation_obj.season, season_obj)
        self.assertEqual(affiliation_obj.player, player_obj)
        self.assertEqual(affiliation_obj.teams.all()[0], team1_obj)
        self.assertEqual(affiliation_obj.teams.all()[1], team2_obj)
        self.assertEqual(affiliation_obj.season.name, self.season)
        self.assertEqual(affiliation_obj.player.name, self.name)
        self.assertEqual(affiliation_obj.player.age, self.age)
        self.assertEqual(affiliation_obj.player.position, self.position)
        self.assertEqual(team2_obj.name, self.teams[1])
        self.assertEqual(team1_obj.name, self.teams[0])
