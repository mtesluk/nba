#!/usr/bin/env python3

'''
stats_scraper - python module for data acquisition

stats are scraped from basketball-reference.com page
stats explanation: https://www.basketball-reference.com/about/glossary.html
artifacts are located in ../data/stats/ directory

usage: python3 scraper.py -s SEASON

'''

import os
import re
import sys
import requests
import csv
from bs4 import BeautifulSoup
import argparse
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

team_shortage_mapper = {
    "BRK": "BKN",
    "CHO": "CHA",
    "PHO": "PHX",
}

team_mapper = {
    "Los Angeles Clippers": "LA Clippers",
}


class StatsScraper:
    def scrape_player_totals(self, season):

        year = season.split('-')[0][:2] + season.split('-')[1]

        stats = ['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA',
                 '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

        URL = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'.format(year)

        file_pattern = 'data/stats/{}/player_stats_{}.csv'.format(season, season)
        outfile = os.path.join(file_pattern)
        if not os.path.isdir(outfile.rsplit('/', 1)[0]):
            os.makedirs(outfile.rsplit('/', 1)[0])
        csv_file = open(outfile, 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(stats)

        logger.info('Getting player totals stats for {} season...'.format(season))

        try:
            r = requests.get(URL)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            sys.exit(1)

        soup = BeautifulSoup(r.text, "html5lib")
        table = soup.find(id="all_totals_stats")
        cells = table.find_all('td')
        cols = len(stats)

        Player  = [cells[i].getText() for i in range( 0, len(cells), cols)]
        Pos     = [cells[i].getText() for i in range( 1, len(cells), cols)]
        Age     = [cells[i].getText() for i in range( 2, len(cells), cols)]
        Tm      = [cells[i].getText() for i in range( 3, len(cells), cols)]
        G       = [cells[i].getText() for i in range( 4, len(cells), cols)]
        GS      = [cells[i].getText() for i in range( 5, len(cells), cols)]
        MP      = [cells[i].getText() for i in range( 6, len(cells), cols)]
        FG      = [cells[i].getText() for i in range( 7, len(cells), cols)]
        FGA     = [cells[i].getText() for i in range( 8, len(cells), cols)]
        FGP     = [cells[i].getText() for i in range( 9, len(cells), cols)]
        THP     = [cells[i].getText() for i in range(10, len(cells), cols)]
        THPA    = [cells[i].getText() for i in range(11, len(cells), cols)]
        THPP    = [cells[i].getText() for i in range(12, len(cells), cols)]
        TWP     = [cells[i].getText() for i in range(13, len(cells), cols)]
        TWPA    = [cells[i].getText() for i in range(14, len(cells), cols)]
        TWPP    = [cells[i].getText() for i in range(15, len(cells), cols)]
        EFGP    = [cells[i].getText() for i in range(16, len(cells), cols)]
        FT      = [cells[i].getText() for i in range(17, len(cells), cols)]
        FTA     = [cells[i].getText() for i in range(18, len(cells), cols)]
        FTP     = [cells[i].getText() for i in range(19, len(cells), cols)]
        ORB     = [cells[i].getText() for i in range(20, len(cells), cols)]
        DRB     = [cells[i].getText() for i in range(21, len(cells), cols)]
        TRB     = [cells[i].getText() for i in range(22, len(cells), cols)]
        AST     = [cells[i].getText() for i in range(23, len(cells), cols)]
        STL     = [cells[i].getText() for i in range(24, len(cells), cols)]
        BLK     = [cells[i].getText() for i in range(25, len(cells), cols)]
        TOV     = [cells[i].getText() for i in range(26, len(cells), cols)]
        PF      = [cells[i].getText() for i in range(27, len(cells), cols)]
        PTS     = [cells[i].getText() for i in range(28, len(cells), cols)]

        Player = [i.replace('*', '') for i in Player]  # Remove possible asterix from player name

        for i in range(0, int(len(cells) / cols)):
            team_shortage = team_shortage_mapper.get(Tm[i], Tm[i])
            row = [Player[i], Pos[i], Age[i], team_shortage, G[i], GS[i], MP[i], FG[i], FGA[i], FGP[i], THP[i], THPA[i], THPP[i], TWP[i], TWPA[i],
                   TWPP[i], EFGP[i], FT[i], FTA[i], FTP[i], ORB[i], DRB[i], TRB[i], AST[i], STL[i], BLK[i], TOV[i], PF[i], PTS[i]]
            csv_writer.writerow(row)

        logger.info('DONE')

    def scrape_player_advanced(self, season):

        year = season.split('-')[0][:2] + season.split('-')[1]

        stats = ['Player', 'Pos', 'Age', 'Tm', 'G', 'MP', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%',
                 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']

        URL = 'https://www.basketball-reference.com/leagues/NBA_{}_advanced.html'.format(year)

        file_pattern = 'data/stats/{}/advplayer_stats_{}.csv'.format(season, season)
        outfile = os.path.join(file_pattern)
        csv_file = open(outfile, 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(stats)

        logger.info('Getting advanced player stats for {} season...'.format(season))

        try:
            r = requests.get(URL)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            sys.exit(1)

        soup = BeautifulSoup(r.text, "html5lib")
        table = soup.find(id="all_advanced_stats")
        cells = table.find_all('td')
        cols = len(stats) + 2  # plus 2 because there are two columns missing!

        Player  = [cells[i].getText() for i in range( 0, len(cells), cols)]
        Pos     = [cells[i].getText() for i in range( 1, len(cells), cols)]
        Age     = [cells[i].getText() for i in range( 2, len(cells), cols)]
        Tm      = [cells[i].getText() for i in range( 3, len(cells), cols)]
        G       = [cells[i].getText() for i in range( 4, len(cells), cols)]
        MP      = [cells[i].getText() for i in range( 5, len(cells), cols)]
        PER     = [cells[i].getText() for i in range( 6, len(cells), cols)]
        TSP     = [cells[i].getText() for i in range( 7, len(cells), cols)]
        TPAr    = [cells[i].getText() for i in range( 8, len(cells), cols)]
        FTr     = [cells[i].getText() for i in range( 9, len(cells), cols)]
        ORBP    = [cells[i].getText() for i in range(10, len(cells), cols)]
        DRBP    = [cells[i].getText() for i in range(11, len(cells), cols)]
        TRBP    = [cells[i].getText() for i in range(12, len(cells), cols)]
        ASTP    = [cells[i].getText() for i in range(13, len(cells), cols)]
        STLP    = [cells[i].getText() for i in range(14, len(cells), cols)]
        BLKP    = [cells[i].getText() for i in range(15, len(cells), cols)]
        TOVP    = [cells[i].getText() for i in range(16, len(cells), cols)]
        USGP    = [cells[i].getText() for i in range(17, len(cells), cols)]
        OWS     = [cells[i].getText() for i in range(19, len(cells), cols)]  # 18 is empty!
        DWS     = [cells[i].getText() for i in range(20, len(cells), cols)]
        WS      = [cells[i].getText() for i in range(21, len(cells), cols)]
        WS48    = [cells[i].getText() for i in range(22, len(cells), cols)]
        OBPM    = [cells[i].getText() for i in range(24, len(cells), cols)]  # 23 is empty!
        DBPM    = [cells[i].getText() for i in range(25, len(cells), cols)]
        BPM     = [cells[i].getText() for i in range(26, len(cells), cols)]
        VORP    = [cells[i].getText() for i in range(27, len(cells), cols)]

        Player = [i.replace('*', '') for i in Player]  # Remove possible asterix from player name

        for i in range(0, int(len(cells) / cols)):
            team_shortage = team_shortage_mapper.get(Tm[i], Tm[i])
            row = [Player[i], Pos[i], Age[i], team_shortage, G[i], MP[i], PER[i], TSP[i], TPAr[i], FTr[i], ORBP[i], DRBP[i], TRBP[i],
                   ASTP[i], STLP[i], BLKP[i], TOVP[i], USGP[i], OWS[i], DWS[i], WS[i], WS48[i], OBPM[i], DBPM[i], BPM[i], VORP[i]]
            csv_writer.writerow(row)

        logger.info('DONE')

    def scrape_team_stats(self, season):

        year = season.split('-')[0][:2] + season.split('-')[1]

        stats = ['Team', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
                 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

        URL = 'https://www.basketball-reference.com/leagues/NBA_{}.html'.format(year)

        file_pattern = 'data/stats/{}/team_stats_{}.csv'.format(season, season)
        outfile = os.path.join(file_pattern)
        csv_file = open(outfile, 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(stats)

        logger.info('Getting team stats for {} season...'.format(season))

        try:
            r = requests.get(URL)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            sys.exit(1)

        soup = BeautifulSoup(r.text, "html5lib")
        table_text = soup.find(text=re.compile('table class="sortable stats_table" id="team-stats-base"'))
        table_soup = BeautifulSoup(table_text, "html5lib")
        cells = table_soup.find_all('td')
        cols = len(stats)

        Team = [cells[i].getText() for i in range( 0, len(cells), cols)]
        G    = [cells[i].getText() for i in range( 1, len(cells), cols)]
        MP   = [cells[i].getText() for i in range( 2, len(cells), cols)]
        FG   = [cells[i].getText() for i in range( 3, len(cells), cols)]
        FGA  = [cells[i].getText() for i in range( 4, len(cells), cols)]
        FGP  = [cells[i].getText() for i in range( 5, len(cells), cols)]
        THP  = [cells[i].getText() for i in range( 6, len(cells), cols)]
        THPA = [cells[i].getText() for i in range( 7, len(cells), cols)]
        THPP = [cells[i].getText() for i in range( 8, len(cells), cols)]
        TWP  = [cells[i].getText() for i in range( 9, len(cells), cols)]
        TWPA = [cells[i].getText() for i in range(10, len(cells), cols)]
        TWPP = [cells[i].getText() for i in range(11, len(cells), cols)]
        FT   = [cells[i].getText() for i in range(12, len(cells), cols)]
        FTA  = [cells[i].getText() for i in range(13, len(cells), cols)]
        FTP  = [cells[i].getText() for i in range(14, len(cells), cols)]
        ORB  = [cells[i].getText() for i in range(15, len(cells), cols)]
        DRB  = [cells[i].getText() for i in range(16, len(cells), cols)]
        TRB  = [cells[i].getText() for i in range(17, len(cells), cols)]
        AST  = [cells[i].getText() for i in range(18, len(cells), cols)]
        STL  = [cells[i].getText() for i in range(19, len(cells), cols)]
        BLK  = [cells[i].getText() for i in range(20, len(cells), cols)]
        TOV  = [cells[i].getText() for i in range(21, len(cells), cols)]
        PF   = [cells[i].getText() for i in range(22, len(cells), cols)]
        PTS  = [cells[i].getText() for i in range(23, len(cells), cols)]

        Team = [i.replace('*', '') for i in Team]  # Remove possible asterix from team name

        for i in range(0, int(len(cells) / cols) - 1):
            team = team_mapper.get(Team[i], Team[i])
            row = [team, G[i], MP[i], FG[i], FGA[i], FGP[i], THP[i], THPA[i], THPP[i], TWP[i], TWPA[i], TWPP[i],
                   FT[i], FTA[i], FTP[i], ORB[i], DRB[i], TRB[i], AST[i], STL[i], BLK[i], TOV[i], PF[i], PTS[i]]
            csv_writer.writerow(row)

        logger.info('DONE')

    def scrape_team_miscellaneous_stats(self, season):

        year = season.split('-')[0][:2] + season.split('-')[1]

        stats = ['Team', 'Age', 'W', 'L', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'NRtg', 'Pace', 'FTr', '3PAr', 'TS%',
                 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'OPP_eFG%', 'OPP_TOV%', 'OPP_DRB%', 'OPP_FT/FGA', 'Arena', 'Att', 'Att/G']

        URL = 'https://www.basketball-reference.com/leagues/NBA_{}.html'.format(year)

        file_pattern = 'data/stats/{}/teammisc_stats_{}.csv'.format(season, season)
        outfile = os.path.join(file_pattern)
        csv_file = open(outfile, 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(stats)

        logger.info('Getting miscellaneous team stats for {} season...'.format(season))

        try:
            r = requests.get(URL)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            sys.exit(1)

        soup = BeautifulSoup(r.text, "html5lib")
        table_text = soup.find(text=re.compile('table class="sortable stats_table" id="misc_stats"'))
        table_soup = BeautifulSoup(table_text, "html5lib")
        cells = table_soup.find_all('td')
        cols = len(stats)

        Team     = [cells[i].getText() for i in range( 0, len(cells), cols)]
        Age      = [cells[i].getText() for i in range( 1, len(cells), cols)]
        W        = [cells[i].getText() for i in range( 2, len(cells), cols)]
        L        = [cells[i].getText() for i in range( 3, len(cells), cols)]
        PW       = [cells[i].getText() for i in range( 4, len(cells), cols)]
        PL       = [cells[i].getText() for i in range( 5, len(cells), cols)]
        MOV      = [cells[i].getText() for i in range( 6, len(cells), cols)]
        SOS      = [cells[i].getText() for i in range( 7, len(cells), cols)]
        SRS      = [cells[i].getText() for i in range( 8, len(cells), cols)]
        ORtg     = [cells[i].getText() for i in range( 9, len(cells), cols)]
        DRtg     = [cells[i].getText() for i in range(10, len(cells), cols)]
        NRtg     = [cells[i].getText() for i in range(11, len(cells), cols)]
        Pace     = [cells[i].getText() for i in range(12, len(cells), cols)]
        FTr      = [cells[i].getText() for i in range(13, len(cells), cols)]
        TPAr     = [cells[i].getText() for i in range(14, len(cells), cols)]
        TSP      = [cells[i].getText() for i in range(15, len(cells), cols)]
        EFGP     = [cells[i].getText() for i in range(16, len(cells), cols)]
        TOVP     = [cells[i].getText() for i in range(17, len(cells), cols)]
        ORBP     = [cells[i].getText() for i in range(18, len(cells), cols)]
        FTPFGA   = [cells[i].getText() for i in range(19, len(cells), cols)]
        O_EFGP   = [cells[i].getText() for i in range(20, len(cells), cols)]
        O_TOVP   = [cells[i].getText() for i in range(21, len(cells), cols)]
        O_DRBP   = [cells[i].getText() for i in range(22, len(cells), cols)]
        O_FTPFGA = [cells[i].getText() for i in range(23, len(cells), cols)]
        Arena    = [cells[i].getText() for i in range(24, len(cells), cols)]
        Att      = [cells[i].getText() for i in range(25, len(cells), cols)]
        AttG     = [cells[i].getText() for i in range(26, len(cells), cols)]

        Team = [i.replace('*', '') for i in Team]  # Remove possible asterix from team name
        Att  = [i.replace(',', '') for i in Att]   # Remove comma from Attendence
        AttG = [i.replace(',', '') for i in AttG]  # Remove comma from Attendence per Game
        Att  = [i.replace('"', '') for i in Att]   # Remove quotes from Attendence
        AttG = [i.replace('"', '') for i in AttG]  # Remove quotes from Attendence per Game
        NRtg = [i.replace('+', '') for i in NRtg]  # Remove pluses from NRtg

        for i in range(0, int(len(cells) / cols) - 1):
            team = team_mapper.get(Team[i], Team[i])
            row = [team, Age[i], W[i], L[i], PW[i], PL[i], MOV[i], SOS[i], SRS[i], ORtg[i], DRtg[i], NRtg[i], Pace[i], FTr[i], TPAr[i], TSP[i],
                   EFGP[i], TOVP[i], ORBP[i], FTPFGA[i], O_EFGP[i], O_TOVP[i], O_DRBP[i], O_FTPFGA[i], Arena[i], Att[i], AttG[i]]
            csv_writer.writerow(row)

        logger.info('DONE')

    def scrape_rookie_stats(self, season):

        year = season.split('-')[0][:2] + season.split('-')[1]

        stats = ['Player', 'Debut', 'Age', 'Yrs', 'G', 'MP', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'TRB',
                 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'FG%', '3P%', 'FT%', 'MP/G', 'PTS/G', 'TRB/G', 'AST/G']

        URL = 'https://www.basketball-reference.com/leagues/NBA_{}_rookies.html'.format(year)

        file_pattern = 'data/stats/{}/rookie_stats_{}.csv'.format(season, season)
        outfile = os.path.join(file_pattern)
        csv_file = open(outfile, 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(stats)

        logger.info('Getting rookie stats for {} season...'.format(season))

        try:
            r = requests.get(URL)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            sys.exit(1)

        soup = BeautifulSoup(r.text, "html5lib")
        table = soup.find(id="rookies")
        cells = table.find_all('td')
        cols = len(stats)

        Player = [cells[i].getText() for i in range( 0, len(cells), cols)]
        Debut  = [cells[i].getText() for i in range( 1, len(cells), cols)]
        Age    = [cells[i].getText() for i in range( 2, len(cells), cols)]
        Yrs    = [cells[i].getText() for i in range( 3, len(cells), cols)]
        G      = [cells[i].getText() for i in range( 4, len(cells), cols)]
        MP     = [cells[i].getText() for i in range( 5, len(cells), cols)]
        FG     = [cells[i].getText() for i in range( 6, len(cells), cols)]
        FGA    = [cells[i].getText() for i in range( 7, len(cells), cols)]
        THP    = [cells[i].getText() for i in range( 8, len(cells), cols)]
        THPA   = [cells[i].getText() for i in range( 9, len(cells), cols)]
        FT     = [cells[i].getText() for i in range(10, len(cells), cols)]
        FTA    = [cells[i].getText() for i in range(11, len(cells), cols)]
        ORB    = [cells[i].getText() for i in range(12, len(cells), cols)]
        TRB    = [cells[i].getText() for i in range(13, len(cells), cols)]
        AST    = [cells[i].getText() for i in range(14, len(cells), cols)]
        STL    = [cells[i].getText() for i in range(15, len(cells), cols)]
        BLK    = [cells[i].getText() for i in range(16, len(cells), cols)]
        TOV    = [cells[i].getText() for i in range(17, len(cells), cols)]
        PF     = [cells[i].getText() for i in range(18, len(cells), cols)]
        PTS    = [cells[i].getText() for i in range(19, len(cells), cols)]
        FGP    = [cells[i].getText() for i in range(20, len(cells), cols)]
        THPP   = [cells[i].getText() for i in range(21, len(cells), cols)]
        FTP    = [cells[i].getText() for i in range(22, len(cells), cols)]
        MPG    = [cells[i].getText() for i in range(23, len(cells), cols)]
        PTSG   = [cells[i].getText() for i in range(24, len(cells), cols)]
        TRBG   = [cells[i].getText() for i in range(25, len(cells), cols)]
        ASTG   = [cells[i].getText() for i in range(26, len(cells), cols)]

        Player = [i.replace('*', '') for i in Player]  # Remove possible asterix from player name

        for i in range(0, int(len(cells) / cols)):
            row = [Player[i], Debut[i], Age[i], Yrs[i], G[i], MP[i], FG[i], FGA[i], THP[i], THPA[i], FT[i], FTA[i], ORB[i], TRB[i],
                   AST[i], STL[i], BLK[i], TOV[i], PF[i], PTS[i], FGP[i], THPP[i], FTP[i], MPG[i], PTSG[i], TRBG[i], ASTG[i]]
            csv_writer.writerow(row)

        logger.info('DONE')

    def fetch(self, season):
        logger.info('STARTED')
        self.scrape_player_totals(season)
        self.scrape_player_advanced(season)
        self.scrape_team_stats(season)
        self.scrape_team_miscellaneous_stats(season)
        self.scrape_rookie_stats(season)
        logger.info('FINISHED')
