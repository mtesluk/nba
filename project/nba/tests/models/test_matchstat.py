from django.test import TestCase
from nba.models import Season, Team, Match, MatchStat, Stat


class MatchStatTestCase(TestCase):
    def setUp(self):
        self.season_type = 'PO'
        self.season = '2016-17'
        self.date = '2017-05-27'
        self.team_host = 'Philadelphia 76ers'
        self.team_visitor = 'Boston Celtics'
        self.PTS = 110

    def test_matchstat(self):
        season_obj = Season.objects.create(name=self.season)
        team_host = Team.objects.create(name=self.team_host)
        team_visitor = Team.objects.create(name=self.team_visitor)
        stat_obj = Stat.objects.create(name="PTS", type="int")
        match_obj = Match.objects.create(season_type=self.season_type, date=self.date, season=season_obj,
                                         team_host=team_host, team_visitor=team_visitor)
        matchstat_obj = MatchStat.objects.create(team=team_visitor, match=match_obj, stat=stat_obj, value=self.PTS)

        self.assertEqual(matchstat_obj.match.season, season_obj)
        self.assertEqual(matchstat_obj.match.team_host.name, self.team_host)
        self.assertEqual(matchstat_obj.match.team_visitor.name, self.team_visitor)
        self.assertEqual(matchstat_obj.team, team_visitor)
        self.assertEqual(matchstat_obj.match, match_obj)
        self.assertEqual(matchstat_obj.match.season.name, self.season)
        self.assertEqual(matchstat_obj.match.season_type, self.season_type)
        self.assertEqual(matchstat_obj.match.date, self.date)
        self.assertEqual(matchstat_obj.match.team_host, team_host)
        self.assertEqual(matchstat_obj.match.team_visitor, team_visitor)
        self.assertEqual(matchstat_obj.team.name, self.team_visitor)
        self.assertEqual(matchstat_obj.value, self.PTS)
