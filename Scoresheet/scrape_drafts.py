
import pandas as pd
import sys
import requests
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LEAGUES = [
    'wAL600',
    'wAL601',
    'wAL602',
    'wAL603',
    'wAL604',
    'wAL605',
    'wBL600',
    'wBL601',
    'wNL600',
    'wNL601',
    'wNL602',
    'wNL603',
    'wNL604',
    'wNL605',
    ]

my_league = 'wBL600'

player_dict = {}
driver = webdriver.Chrome()

for league in LEAGUES:
    url = 'http://www.scoresheet.com/htm-lib/picks.htm?dir_lgw=/FOR_WWW1/' + league + '#now'
    # draft_page = requests.get(url)
    driver.get(url)
    elem = driver.find_element_by_id('msgs')
    
    regex = r"^Team\s*[0-9]*\s*\((?P<team_name>.*)\).*drafted\s(?P<player_id>[0-9]*)\s*(?P<player_team>[A-Za-z-]*)\s*(?P<player_position>[A-Za-z0-9]*)\s*(?P<player_name>[A-Za-z\S]*\s[A-Za-z\S]*)"
    matches = re.finditer(regex, elem.text, re.MULTILINE)
    
    for match_num, match in enumerate(matches, start=1):
        current_player = {
            'name': match.group('player_name'),
            'position': match.group('player_position'),
            'team': match.group('player_team'),
            'available': True,
            'taken_BL': False,
            }
        player_id = match.group('player_id')
        if league.startswith('wNL'):
            player_id = str(int(player_id) + 1000)

        if player_id in player_dict:
            player_dict[player_id]['leagues_taken'].append(league)
        else:
            current_player['leagues_taken'] = [league]
            player_dict[player_id] = current_player

        if league == my_league:
            player_dict[player_id]['available'] = False

        if league.startswith('wBL'):
            player_dict[player_id]['taken_BL'] = True


player_list = []
list_columns = ['id', 'name', 'team', 'position', 'leagues_taken', 'num_leagues_taken', 'available', 'taken_BL']
for key, value in player_dict.items():
    player = {}
    for column in list_columns:
        if column == 'id':
            player[column] = key
        elif column == 'num_leagues_taken':
            player[column] = len(value['leagues_taken'])
        else:
            player[column] = value[column]

    player_list.append(player)


driver.close()
players_df = pd.DataFrame(player_list)
players_df.to_csv('scrape_draft_results.csv', columns=list_columns, index=False)