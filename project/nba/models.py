from django.db import models
from django.db import IntegrityError


class Stat(models.Model):
    STAT_TYPES = (
        ('int', 0),
        ('float', 1),
        ('string', 2),
    )

    name = models.CharField(max_length=10)
    type = models.CharField(max_length=10, choices=STAT_TYPES)

    def __str__(self):
        return "{} - {}".format(self.name, self.get_type_display())


class Season(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Player(models.Model):
    POSITIONS = (
        ('PG', 'Point Guard'),
        ('SG', 'Shootin Guard'),
        ('SF', 'Small Forward'),
        ('PF', 'Power Forward'),
        ('C', 'Center'),
    )

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=2, choices=POSITIONS)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Affiliation(models.Model):
    season = models.ForeignKey(Season, related_name="affiliations", null=True, on_delete=models.SET_NULL)
    player = models.ForeignKey(Player, related_name="affiliations", null=True, on_delete=models.SET_NULL)
    teams = models.ManyToManyField(Team, related_name='affiliations')

    def __str__(self):
        return "%s with %s in %s" % (self.player.name, self.season.name, ", ".join([team.name for team in self.teams.all()]))


class PlayerStat(models.Model):
    player = models.ForeignKey(Player, related_name="stats", null=True, on_delete=models.SET_NULL)
    match = models.ForeignKey('Match', related_name="player_stats", null=True, on_delete=models.SET_NULL)
    season = models.ForeignKey(Season, related_name="player_stats", null=True, on_delete=models.SET_NULL)
    stat = models.ForeignKey(Stat, related_name='player_stats', null=True, on_delete=models.SET_NULL)
    value = models.CharField(max_length=20)

    def __str__(self):
        return "{} for {} in {}".format(self.stat.name, self.player.name, self.season.name)


class TeamStat(models.Model):
    team = models.ForeignKey(Team, related_name="stats", null=True, on_delete=models.SET_NULL)
    season = models.ForeignKey(Season, related_name="team_stats", null=True, on_delete=models.SET_NULL)
    stat = models.ForeignKey(Stat, related_name='team_stats', null=True, on_delete=models.SET_NULL)
    value = models.CharField(max_length=20)

    def __str__(self):
        return "{} for {} in {}".format(self.stat.name, self.team.name, self.season.name)


class Match(models.Model):
    SEASON_TYPES = (
        ('RS', 'Regular Season'),
        ('PO', 'Play Off'),
    )

    season_type = models.CharField(max_length=2, choices=SEASON_TYPES)
    season = models.ForeignKey(Season, related_name='matches', null=True, on_delete=models.SET_NULL)
    date = models.DateField()
    team_host = models.ForeignKey(Team, related_name='host_matches', null=True, on_delete=models.SET_NULL)
    team_visitor = models.ForeignKey(Team, related_name='visitor_matches', null=True, on_delete=models.SET_NULL)

    def get_opponent(self, team):
        """
            team_instance = Team.objects.get(name="xxx")
            match_instance = Match.objects.filter(date"xxx")[0]
            match_instance.get_opponent(team_instance)
        """

        if isinstance(team, Team):
            return self.team_visitor if self.team_host == team else self.team_host
        else:
            raise IntegrityError("Only Team model is allowed...")

    def __str__(self):
        return "{} - {} vs {} in {}".format(self.id, self.team_host.name, self.team_visitor, self.date)


class MatchStat(models.Model):
    team = models.ForeignKey(Team, related_name='match_stats', null=True, on_delete=models.SET_NULL)
    match = models.ForeignKey(Match, related_name='match_stats', null=True, on_delete=models.SET_NULL)
    stat = models.ForeignKey(Stat, related_name='match_stats', null=True, on_delete=models.SET_NULL)
    value = models.CharField(max_length=20, null=False)

    def __str__(self):
        return "{} for {} match in {}".format(self.stat.name, self.team.name, self.match.season.name)
