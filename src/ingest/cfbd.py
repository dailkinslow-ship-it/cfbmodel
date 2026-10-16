import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from src.config import ROOT, load_config

# Settings: loaded once, when this file is first imported
load_dotenv(ROOT / ".env")
CONFIG = load_config()
BASE_URL = CONFIG["api"]["base_url"]
MIN_REMAINING = CONFIG["api"]["min_calls_remaining"]


def fetch(endpoint, params, out_path):
    """Call one CFBD endpoint, save the raw JSON, and return the data.

    Skips the API call if out_path already exists (pull once).
    """
    out_path = Path(out_path)

    # 1. Pull once: if the file already exists, read it instead of calling the API
    if out_path.exists():
        print(f"Skip (already have): {out_path.name}")
        with open(out_path, encoding="utf-8") as f:
            return json.load(f)

    # 2. API key (from your old script)
    api_key = os.getenv("CFBD_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found. Please ensure the API key is in the .env file.")

    # 3. Call the API (from your old script, generalized)
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, params=params, headers=headers, timeout=60)

    if response.status_code != 200:
        raise RuntimeError(f"{endpoint} {params} failed: {response.status_code} {response.text}")

    data = response.json()

    # 4. Save first, so a call we paid for is never lost (from your old script)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # 5. Budget check: stop the whole run if we're near the monthly limit
    remaining = int(response.headers.get("X-CallLimit-Remaining", -1))              
    print(f"Pulled {endpoint} {params}: {len(data)} rows, {remaining} calls left")
    if 0 <= remaining < MIN_REMAINING:
        raise RuntimeError(f"Only {remaining} calls left (floor {MIN_REMAINING}). Stopping.")

    return data