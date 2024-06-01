import io
import os
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

import httpx
from loguru import logger

CURRENT_FILE_PATH = Path(__file__).resolve()
DB_GENERIC_PATH = CURRENT_FILE_PATH.parent.parent.parent / "db"
DB_FOLDER_NAME = "{time}"
CARD_DB_DOWNLOAD_URL = "https://mtgjson.com/api/v5/AllPrintings.sqlite.zip"
AUTO_UPDATE_DB = True
AUTO_UPDATE_DB_INTERVAL = 24 * 7  # in hours

logger.disable("mtgcdb")


def download_card_definitions_db() -> Path:
    """Download card definitions DB"""
    logger.info(f"Downloading card definitions DB from {CARD_DB_DOWNLOAD_URL}")
    response = httpx.get(CARD_DB_DOWNLOAD_URL)
    if response.status_code != 200:
        logger.error(
            f"Failed to download card definitions DB. Status code: {response.status_code}"
        )
        raise Exception("Failed to download card definitions DB")

    zip_db = ZipFile(io.BytesIO(response.content))
    current_time = datetime.now().strftime("%Y%m%dT%H%M%S")
    db_folder_path = DB_GENERIC_PATH / DB_FOLDER_NAME.format(time=current_time)
    db_folder_path.mkdir(parents=True, exist_ok=True)
    zip_db.extractall(path=db_folder_path)
    db_path = db_folder_path / "AllPrintings.sqlite"

    if os.path.exists(db_path):
        logger.success(f"Card definitions saved to {db_path}")
    else:
        raise Exception("Failed to extract card definitions DB")

    return db_path


def get_most_recent_db() -> Path | None:
    """Get the most recent card definitions DB"""
    DB_GENERIC_PATH.mkdir(parents=True, exist_ok=True)
    db_folders = os.listdir(DB_GENERIC_PATH)
    if not db_folders:
        return None

    db_folders.sort()
    latest_db_folder = db_folders[-1]
    latest_db_folder_path = DB_GENERIC_PATH / latest_db_folder
    db_files = os.listdir(latest_db_folder_path)
    if not db_files:
        return None

    db_files.sort()
    latest_db_file = db_files[0]
    latest_db_file_path = latest_db_folder_path / latest_db_file
    return latest_db_file_path


def clean_old_dbs() -> None:
    """Clean old card definitions DBs"""
    db_folders = os.listdir(DB_GENERIC_PATH)
    if not db_folders:
        return

    db_folders.sort()
    for db_folder in db_folders[:-1]:
        db_folder_path = DB_GENERIC_PATH / db_folder
        logger.info(f"Removing old card definitions DB: {db_folder_path}")
        # Remove the folder and its contents
        for file in db_folder_path.iterdir():
            file.unlink()
        db_folder_path.rmdir()


def update_or_pass() -> Path:
    """Check if the card definitions DB should be updated.
    Returns the path to the most recent DB. If no DB is found, download a new one."""

    db_path = get_most_recent_db()
    if not db_path:
        logger.info("No card definitions DB found")
        return download_card_definitions_db()

    latest_db_folder = db_path.parent.name
    db_file_time = datetime.strptime(latest_db_folder, "%Y%m%dT%H%M%S")
    time_diff = datetime.now() - db_file_time
    time_diff_hours = time_diff.total_seconds() / 3600

    if time_diff_hours >= AUTO_UPDATE_DB_INTERVAL and AUTO_UPDATE_DB:
        logger.info(
            f"Updating card definitions DB. Last updated {time_diff_hours/7:.2f} days ago"
        )
        clean_old_dbs()
        return download_card_definitions_db()
    else:
        logger.info(
            f"Skipping card definitions DB update. Last updated {time_diff_hours/7:.2f} days ago"
        )
        return db_path
