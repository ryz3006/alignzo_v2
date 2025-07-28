import os
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent / "config"
CONFIG_FILE = CONFIG_DIR / "config.txt"

DEFAULTS = {
    "LOG_FILE_PATH": "logs/audit.log",
    "LOG_ROTATION_WHEN": "midnight",
    "LOG_ROTATION_INTERVAL": 1,
    "LOG_BACKUP_COUNT": 7,
    "LOG_ARCHIVE_PATH": "logs/archive/",
    "LOG_PURGE_DAYS": 30,
}

def parse_config_file():
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip()
    return config

RAW_FILE_CONFIG = parse_config_file()

CONFIG = {}
SOURCES = {}
for k, default in DEFAULTS.items():
    if k in RAW_FILE_CONFIG:
        v = RAW_FILE_CONFIG[k]
        # Convert to int if needed
        if isinstance(default, int):
            v = int(v)
        CONFIG[k] = v
        SOURCES[k] = f"config.txt ({CONFIG_FILE})"
    elif os.getenv(k) is not None:
        v = os.getenv(k)
        if isinstance(default, int):
            v = int(v)
        CONFIG[k] = v
        SOURCES[k] = "env"
    else:
        CONFIG[k] = default
        SOURCES[k] = "default"

LOG_FILE_PATH = CONFIG["LOG_FILE_PATH"]
LOG_ROTATION_WHEN = CONFIG["LOG_ROTATION_WHEN"]
LOG_ROTATION_INTERVAL = CONFIG["LOG_ROTATION_INTERVAL"]
LOG_BACKUP_COUNT = CONFIG["LOG_BACKUP_COUNT"]
LOG_ARCHIVE_PATH = CONFIG["LOG_ARCHIVE_PATH"]
LOG_PURGE_DAYS = CONFIG["LOG_PURGE_DAYS"]

def print_config():
    print("[Logging Service Config]")
    for k, v in CONFIG.items():
        print(f"  {k}: {v}  (source: {SOURCES[k]})")
    if CONFIG_FILE.exists():
        print(f"Loaded config from: {CONFIG_FILE}")
    else:
        print("No config.txt found, using env or defaults.") 