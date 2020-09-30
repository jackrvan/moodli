import os
import sqlite3

MOODS_DB = os.path.join(os.path.dirname(__file__), 'moods.db')

class dbopen(object):
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
