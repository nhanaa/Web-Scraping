from bs4 import BeautifulSoup as bs
import requests as rq
import re
import pandas as pd

url = "https://lol.fandom.com/wiki/"
player_ID = input("Enter the player's ID: ")

full_url = url + player_ID

r = rq.get(full_url)

player_page = bs(r.content, "html.parser")
# print(player_page.prettify())

# Scrape the info table
infos_table = player_page.find_all("table", attrs={"id":"infoboxPlayer"})[0]
# print(infos_table.prettify())

# Scrape all info labels
infos_boxes = infos_table.select("td.infobox-label")
infos_labels = ["Player ID"] + [label.string for label in infos_boxes if label]

# Scrape all infos
infos = [player_ID] + [label.next_sibling.get_text() for label in infos_boxes]

# Scrape favorite champs
champ_list = infos_table.select("span.champion-sprite")
fav_champs = [champ["title"] for champ in champ_list]

# Add favorite champs to infos
fav_champs_str = ""
for chmp in fav_champs:
    fav_champs_str += (chmp + ",")

infos[8] = fav_champs_str

# Make a panda table

# Make columns
cols_names = infos_labels
cols_names
# print(len(cols_names))

# Make rows
rows = infos
# print(len(rows))

# Make the table
df = pd.DataFrame([rows], columns=cols_names)
df.head(2)

df.to_csv("League.csv", index=False)