import pandas as pd
import sys
import requests
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if len(sys.argv) != 2:
    print("Not a valid request, please pass the CSV_Path")
    sys.exit(2)

CSV_PATH = sys.argv[1]

df = pd.read_csv(CSV_PATH)
column_order = list(df)
# driver = webdriver.Chrome()

players = []

for index, row in df.iterrows():
    id = row['ID']
    base_url = "https://www.baseball-reference.com/players"
    ending = "/" + id[0] + "/" + id + ".shtml"
    player_page = requests.get(base_url + ending)

    bats_text = ""
    regex = r"Bats:.*strong>(?P<BATS>.*)\s"
    matches = re.finditer(regex, player_page.text, re.MULTILINE)
    for match_num, match in enumerate(matches, start=1):
        bats_text = match.group('BATS')
    print(index)

    player = row.to_dict()
    player['Bats'] = bats_text
    players.append(player)

    # driver.get(base_url + ending)
    # elem = driver.find_element_by_xpath('//*[@id="meta"]/div[2]/p[2]')
    # print(elem.text)

column_order.append('Bats')
player_df = pd.DataFrame(players)
player_df.to_csv('output.csv', columns=column_order, index=False)
# driver.close()
