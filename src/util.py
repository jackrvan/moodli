import logging
import os
import sqlite3
import pysftp

from src.constants import TEMP_DB_PATH


def configure_logging(debug):
    logger = logging.getLogger("moodli_logger")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if debug else logging.INFO)

    formatter = logging.Formatter('%(message)s')

    ch.setFormatter(formatter)

    logger.addHandler(ch)

def put_db_back(options):
    logger = logging.getLogger('moodli_logger')
    if os.path.exists(TEMP_DB_PATH):
        with pysftp.Connection(host=options['server_ip'],
                                username=options['server_username'],
                                password=options['server_password']) as sftp:
            logger.debug("Putting db back. Copying %s to %s", TEMP_DB_PATH, options['original_db_path'])
            sftp.put(TEMP_DB_PATH, options['original_db_path'])

def mood_type(mood):
    """Tests to make sure we get an int between 1 and 10 via argparse

    Args:
        mood (str): The input we want to test

    Raises:
        argparse.ArgumentTypeError: Raise if we do not have an integer or its not between 1 and 10

    Returns:
        int: The input we were given casted to an int.
    """
    try:
        mood = int(mood)
        if mood < 1 or mood > 10:
            raise argparse.ArgumentTypeError("Mood must be between 1 and 10")
        return mood
    except ValueError as value_error:
        raise argparse.ArgumentTypeError("Mood must be an integer") from value_error

class dbopen():
    """Simple context manager for opening a database file. Automatically commits and exits
    """
    def __init__(self, fileName):
        self.path = fileName
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()
