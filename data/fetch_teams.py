from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

# Teams
teams_path = "teams.txt"
teams_list = []
with open(teams_path, 'r') as f:
    teams_data = f.readlines()
    for row in teams_data:
        teams_list.append(row.strip())

# Scrape
for team in teams_list:
    try:
        team_name = "_".join(team.strip().split(" "))
        url = "http://en.wikipedia.org/wiki/{}_national_football_team#Players".format(team_name)
        content = urlopen(url).read()
        soup = BeautifulSoup(content)
        tables = soup.find_all('table')

        players_table_idx = 0
        for i, table in enumerate(tables):
            if "Date of birth (age)" in table.text:
                players_table_idx = i
                break

        players_table = tables[players_table_idx]
        players_df = pd.read_html(str(players_table), header=0)[0]
        players_df.to_csv("players_{}.tsv".format(team_name), sep='\t', index=False)
        print("Successfully pulled data for team {}".format(team))
    except:
        print("Pulling data for team {} failed".format(team))