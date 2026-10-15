import json
from pathlib import Path
from collections import Counter

#Hardcoded path is fine for one-off scripts. Future scripts will read paths from config.
#Run from the repo root, or relative path will not resolve.
path = Path("data/raw/games_2024.json")

with open(path, encoding="utf-8") as f: #Explicit encoding avoids windows errors on names that include non-ascii characters.
    games = json.load(f)

fbs = [
    game for game in games
    if game["homeClassification"] == "fbs" or game["awayClassification"] == "fbs"
]
fbs_season_types = Counter(game["seasonType"] for game in fbs)

null_teams = set()

for game in games:
    if game["homeClassification"] is None:
        null_teams.add(game["homeTeam"])
    if game["awayClassification"] is None:
        null_teams.add(game["awayTeam"])

fbs_teams = set()

for game in games:
    if game["homeClassification"] == "fbs":
        fbs_teams.add(game["homeTeam"])
    if game["awayClassification"] == "fbs":
        fbs_teams.add(game["awayTeam"])

print(f"Total games: {len(games)}")
print(f"FBS games: {len(fbs)}")
print(f"FBS games by season type: {fbs_season_types}")
print(f"Teams with null classification: {len(null_teams)}")
for team in sorted(null_teams):
    print(team)
print(f"FBS teams: {len(fbs_teams)}")
print(f"FBS teams also labeled null: {null_teams & fbs_teams}")