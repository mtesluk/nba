from django.test import TestCase
from nba.models import Season, Team, Match


class MatchTestCase(TestCase):
    def setUp(self):
        self.season_type = 'PO'
        self.season = '2016-17'
        self.date = '2017-05-27'
        self.team_host = 'Philadelphia 76ers'
        self.team_visitor = 'Boston Celtics'

    def test_match(self):
        season_obj = Season.objects.create(name=self.season)
        team_host = Team.objects.create(name=self.team_host)
        team_visitor = Team.objects.create(name=self.team_visitor)
        match_obj = Match.objects.create(season_type=self.season_type, date=self.date, season=season_obj,
                                         team_host=team_host, team_visitor=team_visitor)

        self.assertEqual(match_obj.season, season_obj)
        self.assertEqual(match_obj.team_host, team_host)
        self.assertEqual(match_obj.team_visitor, team_visitor)
        self.assertEqual(match_obj.season.name, self.season)
        self.assertEqual(match_obj.season_type, self.season_type)
        self.assertEqual(match_obj.date, self.date)
        self.assertEqual(match_obj.team_host.name, self.team_host)
        self.assertEqual(match_obj.team_host.name, self.team_host)
