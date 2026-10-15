from pathlib import Path
import yaml

# This file lives at src/config.py. Go up to the repo root.
ROOT = Path(__file__).resolve().parent.parent

def load_config():
    """Read config/settings.yaml and return it as a dictionary."""
    config_path = ROOT / "config" / "settings.yaml"
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    s = config["seasons"]
    if not (s["pull_start"] <= s["dev_start"] <= s["dev_end"] < s["test_start"] <= s["test_end"] <= s["pull_end"]):
        raise ValueError("Season ranges are out of order or overlap: check config/settings.yaml")
    
    return config