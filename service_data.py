import os
import subprocess

PROJECT = 'project/'
STATS = 'scripts/stats_scraper.py'
MATCHES = 'scripts/game_collector.py'
DATA_STATS = 'project/data/stats/{}'
DATA_MATCHES = 'project/data/matches-json/{}/{}'


def run_matches():
    season = input('Which season download (2017-18, ...): ')
    type = input('Which type season download [RS/xx]: ')
    subprocess.run(['python3', MATCHES, '-s', season, '-t', type])

def run_stats():
    season = input('Which season download (2017-18, ...): ')
    subprocess.run(['python3', STATS, '-s', season])

def run_both():
    season = input('Which season download (2017-18, ...): ')
    type = input('Which type season download [RS/xx]: ')
    s1 = subprocess.Popen(['python3', STATS, '-s', season])
    s2 = subprocess.Popen(['python3', MATCHES, '-s', season, '-t', type])
    s1.communicate()
    s2.communicate()
    
def data_prepared(season, type):
    find_1 = os.path.isdir(DATA_STATS.format(season))
    find_2 = os.path.isdir(DATA_MATCHES.format(season, type))
    if find_1 and find_2 and season and type:
        return True
    return False

def show_options():
    print("1. Matches")
    print("2. Players and team stats")
    print("3. Both")
    print("4. Back")
    print("5. Exit")

def show_type():
    print("1. Fetch data from web")
    print("2. Insert data to database")
    print("3. Exit")

def manage_option(option):
    if option == '1':
        run_matches()
        exit(1)
    elif option == '2':
        run_stats()
        exit(1)
    elif option == '3':
        run_both()
        exit(1)
    elif option == '4':
        return True
    elif option == '5':
        exit(1)

    return False


def manage_type(type):
    if type == '3':
        exit(1)
    elif type == '2':
        season = input('Which season download (2017-18, ...): ')
        type = input('Which type season download [RS/xx]: ')
        if data_prepared(season, type):
            subprocess.run([
                'python',
                PROJECT + 'manage.py',
                'insert_data',
                '-s', season,
                '-t', type])
        else:
            print('\nMake sure all data is prepared...\n' + \
                  'Files should exists in:\n' + \
                  DATA_STATS.format(season) + '\n' + \
                  DATA_MATCHES.format(season, type))
        exit(1)
    elif type == '1':
        while True:
            subprocess.run(['clear'])
            show_options()
            option = input('Option: ')
            
            if manage_option(option):
                break
    
def run():
    while True:
        subprocess.run(['clear'])
        show_type()
        type = input('Type: ')
        manage_type(type)
    
if __name__ == '__main__':
    run()
    
