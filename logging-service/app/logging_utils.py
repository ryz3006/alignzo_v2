import logging
from logging.handlers import TimedRotatingFileHandler
import os
import shutil
from datetime import datetime, timedelta
from .config import LOG_FILE_PATH, LOG_ROTATION_WHEN, LOG_ROTATION_INTERVAL, LOG_BACKUP_COUNT, LOG_ARCHIVE_PATH, LOG_PURGE_DAYS

def setup_logger():
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    os.makedirs(LOG_ARCHIVE_PATH, exist_ok=True)
    logger = logging.getLogger("audit_logger")
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(
        LOG_FILE_PATH,
        when=LOG_ROTATION_WHEN,
        interval=LOG_ROTATION_INTERVAL,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    logger.addHandler(handler)
    return logger

def archive_and_purge_logs():
    # Archive rotated logs
    for filename in os.listdir(os.path.dirname(LOG_FILE_PATH)):
        if filename.startswith(os.path.basename(LOG_FILE_PATH)) and filename != os.path.basename(LOG_FILE_PATH):
            src = os.path.join(os.path.dirname(LOG_FILE_PATH), filename)
            dst = os.path.join(LOG_ARCHIVE_PATH, filename)
            if not os.path.exists(dst):
                shutil.move(src, dst)
    # Purge old logs
    now = datetime.now()
    for filename in os.listdir(LOG_ARCHIVE_PATH):
        file_path = os.path.join(LOG_ARCHIVE_PATH, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if (now - file_mtime).days > LOG_PURGE_DAYS:
                os.remove(file_path) 