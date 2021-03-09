import os

ENTRY_COLUMNS = {'content': "TEXT", 'mood': "INTEGER", 'sleep': "INTEGER", 'date': "TEXT"}
# Keys are config args and values are examples to use in the create config
KNOWN_CONFIG_ARGS = {
    'server_ip': '192.168.1.2  # OPTIONAL IP of server that holds our database',
    'server_username': 'username  # OPTIONAL Username needed to access the server',
    'server_password': 'password  # OPTIONAL Pasword needed to access the server',
    'database_location': '/home/username/Documents/moodli_database.db  # REQUIRED Path to database'
}
TEMP_DB_PATH = os.path.join('/', 'tmp', 'moodli.db')
