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

# driver = webdriver.Chrome()

for index, row in df.iterrows():
    id = row['ID']
    base_url = "https://www.baseball-reference.com/players"
    ending = "/" + id[0] + "/" + id + ".shtml"
    player_page = requests.get(base_url + ending)
    player_page.json()
    print(player_page)
    bats = re.match("Bats:(\?<BATS>.*)\s", player_page.body)
    print(bats)
    if bats is not None:
        bats_text = bats.group('BATS')
        print(row['Name'] + ": " + bats_text)
    # driver.get(base_url + ending)
    # elem = driver.find_element_by_xpath('//*[@id="meta"]/div[2]/p[2]')
    # print(elem.text)


# driver.close()
