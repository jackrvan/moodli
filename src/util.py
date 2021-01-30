import sqlite3
import logging

def configure_logging(debug):
    logger = logging.getLogger("moodli_logger")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if debug else logging.INFO)

    formatter = logging.Formatter('%(message)s')

    ch.setFormatter(formatter)

    logger.addHandler(ch)


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
