import os
from pathlib import Path
import sys
import pysftp

from src.constants import KNOWN_CONFIG_ARGS

def parse_config():
    options = {}
    with open(os.path.join(str(Path.home()), '.moodli', 'moodli.config'), 'r') as f:
        for knt, line in enumerate(f.readlines(), start=1):
            try:
                option, value = line.strip().split('=')
                if option in KNOWN_CONFIG_ARGS:
                    options[option] = value.strip(' "\n')
                else:
                    print("Option {} on line {} is not a known option. All known options are {}".
                        format(option, knt, ', '.join(KNOWN_CONFIG_ARGS)))
            except ValueError:
                print("Could not parse {} on line {} in config. Please use format a=b".format(line, knt))
                sys.exit(1)
    ConfigSettings(**options)

class ConfigSettings():
    db_path = os.path.join(str(Path.home()), '.moodli', '.moods.db')
    def __init__(self, database_location=None, server_ip=None, server_username=None, server_password=None):
        if server_ip:
            with pysftp.Connection(host=server_ip, username=server_username, 
                password=server_password) as sftp:
                print("Copying database from {} to {} temporarily".format(
                    database_location, os.path.join('/', 'tmp', 'moodli.db')))
                sftp.get(database_location, os.path.join('/', 'tmp', 'moodli.db'))
            ConfigSettings.db_path = os.path.join('/', 'tmp', 'moodli.db')
        elif database_location:
            ConfigSettings.db_path = database_location
