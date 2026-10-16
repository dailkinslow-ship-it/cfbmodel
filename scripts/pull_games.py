from src.config import ROOT, load_config
from src.ingest.cfbd import fetch

config = load_config()
seasons = config["seasons"]
raw_dir = ROOT / config["paths"]["raw"]

for year in range(seasons["pull_start"], seasons["pull_end"]+1):
    fetch("/games", {"year": year}, raw_dir / f"games_{year}.json")