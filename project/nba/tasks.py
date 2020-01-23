from __future__ import absolute_import, unicode_literals
from celery import shared_task

from nba.scripts.stats_scraper import StatsScraper
from nba.scripts.game_collector import GameCollector
from nba.management.commands.insert_data import Command


@shared_task
def download(season, season_type=None):
    if season_type:
        GameCollector().fetch(season, season_type)
    else:
        StatsScraper().fetch(season)
    return 'Task fetch executed'


@shared_task
def insert(season, season_type):
    Command().handle(season=season, season_type=season_type)
    return 'Task instert executed'
