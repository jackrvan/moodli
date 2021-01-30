import os

ENTRY_COLUMNS = {'content': "TEXT", 'mood': "INTEGER", 'sleep': "INTEGER", 'date': "TEXT"}
KNOWN_CONFIG_ARGS = frozenset(['server_ip', 'server_username', 'server_password', 'database_location'])
TEMP_DB_PATH = os.path.join('/', 'tmp', 'moodli.db')
