import os, json
from pathlib import Path
from dotenv import load_dotenv
import requests

# Configuration
SEASON = 2024
BASE_URL = "https://api.collegefootballdata.com"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Load environment variables from .env file and check for the API key
load_dotenv()
api_key = os.getenv("CFBD_API_KEY")

if not api_key:
    raise RuntimeError("API key not found. Please ensure the API key is in the .env file.")

#Request parameters
url = f"{BASE_URL}/games"
params = {"year": SEASON}
headers = {"Authorization": f"Bearer {api_key}"}

#Calling the API
response = requests.get(url, params=params, headers=headers)

# Check for successful response
if response.status_code != 200:
    raise RuntimeError(f"...{response.status_code}...{response.text}...")

#applying the data to the variable games
games = response.json()

RAW_DIR.mkdir(parents=True, exist_ok=True)

# Save the data to a JSON file
out_path = RAW_DIR / f"games_{SEASON}.json"

with open(out_path, "w") as f:
    json.dump(games, f, indent=2)

print(f"Amount of games returned: {len(games)}")
print(f"Data saved to {out_path}")