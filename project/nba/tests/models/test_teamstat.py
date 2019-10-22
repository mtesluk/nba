from django.test import TestCase
from nba.models import Season, Team, TeamStat, Stat


class TeamStatTestCase(TestCase):
    def setUp(self):
        self.team = 'Houston Rockets'
        self.season = '2017-18'
        self.PTS = 9213

    def test_teamstat(self):
        season_obj = Season.objects.create(name=self.season)
        team_obj = Team.objects.create(name=self.team)
        stat_obj = Stat.objects.create(name="PTS", type="int")
        teamstat_obj = TeamStat.objects.create(season=season_obj, team=team_obj, stat=stat_obj, value=self.PTS)

        self.assertEqual(teamstat_obj.season, season_obj)
        self.assertEqual(teamstat_obj.team, team_obj)
        self.assertEqual(teamstat_obj.season.name, self.season)
        self.assertEqual(teamstat_obj.team.name, self.team)
        self.assertEqual(teamstat_obj.value, self.PTS)
