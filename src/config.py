import toml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.toml"
config = toml.load(CONFIG_PATH)

DUMMYJSON_CONFIG = config["dummyjson"]
OPENGAGE_CONFIG = config["opencage"]