#!/usr/bin/env python3

'''
game_collector - python module for game stats acquisition

- uses nba_api and LeagueGameFinder endpoint to get json object with match stats
- more info: https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguegamefinder.md
- artifacts are located in ../data/matches/ directory

usage: python3 game_collector.py -s SEASON -t SEASONTYPE

'''

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import json
import csv
import logging
import argparse
import re
import os
from datetime import datetime
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class GameCollector:

    def fetch(self, season, seasontype):
        regular_season_pattern = re.compile('^RS$')
        if regular_season_pattern.match(seasontype):
            season_type = 'Regular Season'
        else:
            season_type = 'Playoffs'

        nba_dict = {}
        nba_teams = teams.get_teams()

        for team in nba_teams:
            nba_dict[team['abbreviation']] = team['id']

        logger.info('STARTED')

        for team, team_id in nba_dict.items():

            json_pattern = 'data/matches-json/{}/{}/{}_{}_matches.json'.format(season, seasontype, team, season)
            csv_pattern = 'data/matches-csv/{}/{}/{}_{}_matches.csv'.format(season, seasontype, team, season)

            json_outfile = os.path.join(json_pattern)
            csv_outfile = os.path.join(csv_pattern)

            if not os.path.isdir(json_outfile.rsplit('/', 1)[0]):
                os.makedirs(json_outfile.rsplit('/', 1)[0])

            if not os.path.isdir(csv_outfile.rsplit('/', 1)[0]):
                os.makedirs(csv_outfile.rsplit('/', 1)[0])

            logger.info('Getting {} matches for {} {}...'.format(team, season, season_type))

            game_finder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable=season, season_type_nullable=season_type)
            games = game_finder.get_normalized_json()
            games_parsed = json.loads(games)
            json_data = games_parsed["LeagueGameFinderResults"]
            correct_data = []                                   # despite 'Regular Season' param checked, API throws also Summer League results
            date_to_remove = re.compile('\d{4}-07-\d{2}')       # Summer League takes place in July, so issue an be ommitted this way
            for item in json_data:
                if not date_to_remove.match(item["GAME_DATE"]):
                    correct_data.append(item)

            with open(json_outfile, 'w') as f:
                f.write(json.dumps(correct_data))

            with open(csv_outfile, 'w') as f:
                csvwriter = csv.writer(f)
                count = 0
                for item in correct_data:
                    if count == 0:
                        header = item.keys()
                        csvwriter.writerow(header)
                        count += 1
                    csvwriter.writerow(item.values())

            logger.info('DONE!')
            time.sleep(5)

        logger.info('FINISHED')
