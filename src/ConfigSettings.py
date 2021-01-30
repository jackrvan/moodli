import os
from pathlib import Path
import sys
import pysftp
import logging

from src.constants import KNOWN_CONFIG_ARGS, TEMP_DB_PATH

logger = logging.getLogger('moodli_logger')

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
                    logger.error("Option %s on line %s is not a known option. All known options are %s",
                                    option, knt, ', '.join(KNOWN_CONFIG_ARGS))
            except ValueError:
                logger.error("Could not parse %s on line %s in config. Please use format a=b", line, knt)
                sys.exit(1)
    if 'server_ip' in options:
        # Database is stored on a server need to do extra work.
        # Copy the database over from the server to our local machine
        with pysftp.Connection(host=options['server_ip'],
                               username=options['server_username'],
                               password=options['server_password']) as sftp:
            if sftp.exists(options['database_location']):
                logger.debug("Copying database from %s to %s temporarily",
                                options['database_location'], TEMP_DB_PATH)
                sftp.get(options['database_location'], TEMP_DB_PATH)
            else:
                logger.error("No database at %s on remote %s. Creating new db.",
                                options['database_location'], options['server_ip'])
        # Then we save the original db path (path on the server)
        options['original_db_path'] = options['database_location']
        options['database_location'] = TEMP_DB_PATH
    return options
