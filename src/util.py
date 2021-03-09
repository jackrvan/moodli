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

class dbopen():
    """Simple context manager for opening a database file. Automatically commits and exits
    """
    def __init__(self, fileName):
        self.path = fileName
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()
