import sqlite3

ENTRY_COLUMNS = {'content': "TEXT", 'mood': "INTEGER", 'sleep': "INTEGER", 'date': "TEXT"}
KNOWN_CONFIG_ARGS = frozenset(['server_ip', 'server_username', 'server_password', 'database_location'])

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
