import os
from pathlib import Path
import sys
import pysftp

from src.constants import KNOWN_CONFIG_ARGS, TEMP_DB_PATH

def parse_config():
    """Parse the config file located in ~/.moodli/moodli.config
    """
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
                print("Could not parse {} on line {} in config. Please use format a=b"
                      .format(line, knt))
                sys.exit(1)
    if 'server_ip' in options:
        # Database is stored on a server need to do extra work.
        # Copy the database over from the server to our local machine
        with pysftp.Connection(host=options['server_ip'],
                               username=options['server_username'],
                               password=options['server_password']) as sftp:
            print("Copying database from {} to {} temporarily"
                  .format(options['database_location'], TEMP_DB_PATH))
            sftp.get(options['database_location'], TEMP_DB_PATH)
        # Then we save the original db path (path on the server)
        options['original_db_path'] = options['database_location']
        options['database_location'] = TEMP_DB_PATH
    return options
