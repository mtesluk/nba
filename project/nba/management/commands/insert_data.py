from django.core.management.base import BaseCommand
from django.db import transaction
from nba.models import Season, Team, Match, MatchStat, Player, PlayerStat, TeamStat, Affiliation, Stat
from django.utils.dateparse import parse_date
from nba.stat_config import player_stat, team_stat, match_stat
from datetime import datetime, timedelta
import logging
import os
import json
import time
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
log_path = "logs/put_data_to_database{}".format(datetime.now().strftime("%d-%m-%Y-%H:%M:%S"))
if not os.path.isdir(log_path.rsplit('/', 1)[0]):
    os.makedirs(log_path.rsplit('/', 1)[0])
file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Command(BaseCommand):
    help = "Script to insert data from files to database"

    def add_arguments(self, parser):
        parser.add_argument("-s", "--season", type=str, required=True, help="Season of matches etc. -s 2017-18")
        parser.add_argument("-t", "--season-type", type=str, help="Type of season etc. RS, PO")

    @transaction.atomic
    def handle(self, *args, **kwargs):
        season = kwargs["season"]
        season_type = kwargs["season_type"]
        self.teams_shortage = {}
        logger.info('STARTED')

        if not (season and season_type):
            self.stdout.write(self.style.ERROR("Provide args etc. -s 2017-18 -o stats"))
            logger.error('FINISHED by not providing arguments')
            return

        start = time.time()
        season_obj, _ = self._load_new_season(season)
        players_advance_path = "data/stats/%s/advplayer_stats_%s.csv" % (season, season)
        players_path = "data/stats/%s/player_stats_%s.csv" % (season, season)
        teams_advance_path = "data/stats/%s/teammisc_stats_%s.csv" % (season, season)
        teams_path = "data/stats/%s/team_stats_%s.csv" % (season, season)
        matches_path = "data/matches-json/%s/%s/" % (season, season_type)
        match_files = self._get_files(matches_path, ".json")
        self._create_teams_shortage(match_files)
        self._load_teams(match_files)
        self._load_teams_stat(teams_advance_path, teams_path, season_obj)
        self._load_players(players_advance_path, players_path, season_obj)
        self._load_files_matches(match_files, season_obj, season_type)
        end = time.time()
        loading_time = timedelta(seconds=(end - start))
        logger.info('LOADING TIME: %s' % str(loading_time))
        self.stdout.write(self.style.SUCCESS("Database has loaded in %s" % str(loading_time)))
        logger.info('FINISHED')

    def _load_files_matches(self, match_files, season_obj, season_type):
        for f in match_files:
            with open(f, "r") as read_file:
                data = json.load(read_file)
                self._load_matches(data, season_obj, season_type)

    def _load_teams(self, files):
        for f in files:
            with open(f, "r") as read_file:
                data = json.load(read_file)
                try:
                    team = data[0]["TEAM_NAME"]
                    team_abbreviation = data[0]["TEAM_ABBREVIATION"]
                except IndexError:
                    self.stdout.write("Team %s did not play in %s Playoffs!" % (f.split('/')[4].split('_')[0], f.split('_')[1]))
                else:
                    Team.objects.get_or_create(name=team)
                    logger.info("Team %s created..." % team)
                    self.stdout.write(self.style.SQL_KEYWORD("Team %s created..." % team_abbreviation))

    def _load_teams_stat(self, teams_advance_path, teams_path, season_obj):
        with open(teams_advance_path) as read_file_adv_team:
            with open(teams_path) as read_file_team:
                reader_adv_team = csv.DictReader(read_file_adv_team)
                reader_team = csv.DictReader(read_file_team)
                for adv_team_data, team_data in zip(reader_adv_team, reader_team):
                    team_obj = Team.objects.get(name=team_data["Team"])
                    for stat in team_stat:
                        stat_obj, _ = Stat.objects.get_or_create(name=stat['name'], type=stat['type'])
                        TeamStat.objects.create(team=team_obj,
                                                season=season_obj,
                                                stat=stat_obj,
                                                value=self._get_available_value(adv_team_data, team_data, stat['source']))

        logger.info("Teams stats created...")
        self.stdout.write(self.style.SQL_KEYWORD("Teams stats created..."))

    def _load_players(self, players_advance_path, players_path, season_obj):
        player_stat_total_state = {}
        with open(players_advance_path) as read_file_adv_player:
            with open(players_path) as read_file_player:
                reader_adv_player = csv.DictReader(read_file_adv_player)
                reader_player = csv.DictReader(read_file_player)
                for adv_plater_data, player_data in zip(reader_adv_player, reader_player):
                    pos = player_data["Pos"] if "-" not in player_data["Pos"] else player_data["Pos"].split("-")[0].strip()
                    if not Player.objects.filter(name=player_data["Player"]).exists():
                        player_obj = Player.objects.create(name=player_data["Player"],
                                                           position=pos,
                                                           age=player_data["Age"])
                    else:
                        player_obj = Player.objects.get(name=player_data["Player"])
                    logger.info("Player %s created..." % player_obj.name)
                    self.stdout.write(self.style.SQL_KEYWORD("Player %s created..." % player_obj.name))

                    if player_data["Tm"] != "TOT":
                        team_obj = Team.objects.get(name=self.teams_shortage[player_data["Tm"]])
                        self._load_affiliation(team_obj, player_obj, season_obj)

                    self._load_player_stats(player_obj, player_data, adv_plater_data, season_obj, player_stat_total_state)

    def _load_affiliation(self, team_obj, player_obj, season_obj):
        affiliation_obj, _ = Affiliation.objects.get_or_create(player=player_obj, season=season_obj)
        affiliation_obj.teams.add(team_obj)
        logger.info("Affiliation between %s and %s in %s created..." % (player_obj.name, team_obj.name, season_obj.name))
        self.stdout.write(self.style.SQL_KEYWORD("Affiliation between %s and %s in %s created..." % (player_obj.name,
                                                                                                     team_obj.name,
                                                                                                     season_obj.name)))

    def _load_player_stats(self, player_obj, player_data, adv_plater_data, season_obj, player_stat_total_state):
        if player_stat_total_state.get(player_data["Player"], False):
            return

        if player_data["Tm"] == "TOT":
            player_stat_total_state[player_data["Player"]] = True

        for key, value in player_data.items():
            if not value:
                player_data[key] = 0

        for key, value in adv_plater_data.items():
            if not value:
                adv_plater_data[key] = 0

        for stat in player_stat:
            stat_obj, _ = Stat.objects.get_or_create(name=stat['name'], type=stat['type'])
            PlayerStat.objects.create(player=player_obj,
                                      season=season_obj,
                                      stat=stat_obj,
                                      value=self._get_available_value(player_data, adv_plater_data, stat['source']))

    def _load_new_season(self, season):
        season_obj = Season.objects.get_or_create(name=season)
        logger.info("Season %s created..." % season)
        self.stdout.write(self.style.SQL_KEYWORD("Season %s created..." % season))
        return season_obj

    def _load_matches(self, data, season_obj, season_type):
        try:
            team = data[0]["TEAM_NAME"]
        except IndexError:
            pass
        else:
            for data_match in data:
                team_host, team_visitor = self._recognise_teams(data_match["MATCHUP"])
                date = parse_date(data_match["GAME_DATE"])
                match_obj, _ = Match.objects.get_or_create(season=season_obj, season_type=season_type, date=date,
                                                           team_host=team_host, team_visitor=team_visitor)
                self._load_match_stats(data_match, match_obj)
            logger.info("%s matches created..." % team)
            self.stdout.write(self.style.SQL_KEYWORD("%s matches created..." % team))

    def _load_match_stats(self, data, match_obj):
        team_obj = Team.objects.get(name=data["TEAM_NAME"])
        for stat in match_stat:
            stat_obj, _ = Stat.objects.get_or_create(name=stat['name'], type=stat['type'])
            MatchStat.objects.create(team=team_obj,
                                     match=match_obj,
                                     stat=stat_obj,
                                     value=data.get(stat['source'], None))

    def _create_teams_shortage(self, match_files):
        for f in match_files:
            with open(f, "r") as read_file:
                data = json.load(read_file)
                for match in data:
                    self.teams_shortage[match["TEAM_ABBREVIATION"]] = match["TEAM_NAME"]

    def _get_files(self, path, format):
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                if format in file:
                    files.append(os.path.join(r, file))
        return files

    def _recognise_teams(self, data):
        team_list = [data[:3], data[-3:]] if "vs" in data else [data[-3:], data[:3]]
        return [Team.objects.get(name=self.teams_shortage[team]) for team in team_list]

    def _get_available_value(self, data, data_prim, name):
        val = data.get(name, None)
        return val if val is not None else data_prim.get(name, None)
