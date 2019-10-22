from django.test import TestCase
from nba.models import Season, Player, PlayerStat, Stat


class PlayerStatTestCase(TestCase):
    def setUp(self):
        self.player = 'LeBron James'
        self.age = '33'
        self.position = 'SF'
        self.season = '2017-18'
        self.PTS = 2251

    def test_playerstat(self):
        season_obj = Season.objects.create(name=self.season)
        player_obj = Player.objects.create(name=self.player, age=self.age, position=self.position)
        stat_obj = Stat.objects.create(name="PTS", type="int")
        playerstat_obj = PlayerStat.objects.create(season=season_obj, player=player_obj, stat=stat_obj, value=self.PTS)

        self.assertEqual(playerstat_obj.player, player_obj)
        self.assertEqual(playerstat_obj.season, season_obj)
        self.assertEqual(playerstat_obj.player.age, self.age)
        self.assertEqual(playerstat_obj.player.position, self.position)
        self.assertEqual(playerstat_obj.season.name, self.season)
        self.assertEqual(playerstat_obj.value, self.PTS)
