from bs4 import BeautifulSoup as bs
import requests as rq
import re
import pandas as pd
from IPython.display import display

# Create the player group infos list
player_group = []

# Number of players to add
num = int(input("Enter the numbers of players to add: "))

# Adding the players
for i in range(num):
    # Retrieve the web urls
    general_url = "https://lol.fandom.com/wiki/"
    player_ID = input("Enter the player ID: ")

    info_url = general_url + player_ID
    stat_url = info_url + "/Statistics"
    print(info_url)
    print(stat_url)

    # Load the pages
    r1 = rq.get(info_url)
    info_page = bs(r1.content, "html.parser")

    r2 = rq.get(stat_url)
    stat_page = bs(r2.content, "html.parser")

    # Create the columns labels
    column_labels = ["Player ID", "Team", "Birth", "Role", "KDA", "Kill Participation", "Games Played", "Win Rate"]

    # Create info list for each player
    player_info = [player_ID]

    # Get the info box
    info_box = info_page.find("table", attrs={"id":"infoboxPlayer"})

    # Get team info
    team = info_box.select("span.teamname")[0].string
    # Insert the team info
    player_info = player_info + [team]

    # Get birth info
    birth_sib = info_box.find("td", string="Birthday")
    birth = birth_sib.next_sibling.get_text()
    # Insert the birth info
    player_info = player_info + [birth]

    # Get role info
    role_sib = info_box.find("td", string="Role")
    role = role_sib.next_sibling.get_text()
    # Insert the role info
    player_info = player_info + [role]

    # Get overall stats
    stat_overall = stat_page.find("th", string="Overall:").parent.select("th")

    # Get KDA
    KDA = float(stat_overall[8].string)
    # Insert KDA
    player_info = player_info + [KDA]

    # Get Kill Participation
    kill_part_string = stat_overall[13].string
    if len(kill_part_string) > 1:
        kill_part = float(kill_part_string.strip("%")) / 100
    else:
        kill_part = kill_part_string
    # Insert Kill Participation
    player_info = player_info + [kill_part]

    # Get total stats
    stat_total = stat_page.find("th", string="Total:").parent.select("th")

    # Get Games Played
    games_played = int(stat_total[1].string)
    # Insert Games Played
    player_info = player_info + [games_played]

    # Get winrate
    winrate_string = stat_total[4].string
    winrate = float(winrate_string.strip("%")) / 100
    # Insert Winrate
    player_info = player_info + [winrate]

    # Insert player info to the player group info
    player_group = player_group + [player_info]

# Make rows
rows = player_group
# Make the table
df = pd.DataFrame(rows, columns=column_labels)

df.to_csv("LeaguePlayer.csv", index=False)

display(df)