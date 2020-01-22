'''
player_matches - python module for single player's game stats acquisition

- uses nba_api - CommonTeamRoster and PlayerGameLog endpoints to get json object with match stats
- more info: https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/commonteamroster.md
- more info: https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playergamelog.md
- artifacts are located in ../data/player_matches/ directory

usage: python3 player_matches.py -s SEASON -t SEASONTYPE

'''

from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelog
import json
import csv
import time
import os
import logging
import argparse
import re
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

log_path = "logs/player_matches_{}".format(datetime.now().strftime("%d-%m-%Y-%H:%M:%S"))
if not os.path.isdir(log_path.rsplit('/', 1)[0]):
    os.makedirs(log_path.rsplit('/', 1)[0])
file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--season", type=str, required=True, help="season, proper format e.g. 2017-18")
parser.add_argument("-t", "--seasontype", type=str, required=True, help="part of season, Regular Season(RS) or Play-Off(PO)")
args = parser.parse_args()

season = args.season
regular_season_pattern = re.compile('^RS$')
if regular_season_pattern.match(args.seasontype):
    season_type = 'Regular Season'
    season_shortage = 'RS'
else:
    season_type = 'Playoffs'
    season_shortage = 'PO'

nba_dict = {
    'ATL': 1610612737,
    'BOS': 1610612738,
    'CLE': 1610612739,
    'NOP': 1610612740,
    'CHI': 1610612741,
    'DAL': 1610612742,
    'DEN': 1610612743,
    'GSW': 1610612744,
    'HOU': 1610612745,
    'LAC': 1610612746,
    'LAL': 1610612747,
    'MIA': 1610612748,
    'MIL': 1610612749,
    'MIN': 1610612750,
    'BKN': 1610612751,
    'NYK': 1610612752,
    'ORL': 1610612753,
    'IND': 1610612754,
    'PHI': 1610612755,
    'PHX': 1610612756,
    'POR': 1610612757,
    'SAC': 1610612758,
    'SAS': 1610612759,
    'OKC': 1610612760,
    'TOR': 1610612761,
    'UTA': 1610612762,
    'MEM': 1610612763,
    'WAS': 1610612764,
    'DET': 1610612765,
    'CHA': 1610612766
}

data = {}

for team, team_id in nba_dict.items():
    logger.info("Getting roster for {}".format(team))
    roster = commonteamroster.CommonTeamRoster(season=season, team_id=team_id)
    players_raw = roster.data_sets[0].get_dict()
    players = players_raw["data"]
    player_list = []
    for player in players:
        player_list.append([player[i] for i in (3, -1)])  # name and player_id
    data[team] = player_list
    time.sleep(5)

for team, players in data.items():
    team_players_matches = []
    for player in players:
        logger.info("[{}] - getting matches for {}".format(team, player[0]))
        playermatches = playergamelog.PlayerGameLog(player_id=player[1], season=season, season_type_all_star=season_type)
        matches_raw = json.loads(playermatches.get_normalized_json())
        matches = matches_raw['PlayerGameLog']
        matches_list = [match for match in matches]
        for match in matches_list:
            match["Player"] = player[0]
            team_players_matches.append(match)
        time.sleep(5)

    json_pattern = "data/player_matches_json/{}/{}/{}_players_matches.json".format(team, season, season_shortage)
    csv_pattern = "data/player_matches_csv/{}/{}/{}_players_matches.csv".format(team, season, season_shortage)

    json_outfile = os.path.join(json_pattern)
    csv_outfile = os.path.join(csv_pattern)

    if not os.path.isdir(json_outfile.rsplit('/', 1)[0]):
        os.makedirs(json_outfile.rsplit('/', 1)[0])

    if not os.path.isdir(csv_outfile.rsplit('/', 1)[0]):
        os.makedirs(csv_outfile.rsplit('/', 1)[0])

    if team_players_matches == []:
        continue

    with open(json_outfile, 'w') as f:
        json.dump(team_players_matches[:], f)
    keys = team_players_matches[0].keys()
    with open(csv_outfile, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, keys)
        csv_writer.writeheader()
        for match in team_players_matches:
            csv_writer.writerow(match)
