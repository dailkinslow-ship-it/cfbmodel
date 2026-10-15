from pathlib import Path
import yaml

# This file lives at src/config.py. Go up to the repo root.
ROOT = Path(__file__).resolve().parent.parent

def load_config():
    """Read config/settings.yaml and return it as a dictionary."""
    config_path = ROOT / "config" / "settings.yaml"
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config