import argparse
import logging

from src.ConfigSettings import parse_config, write_config_file
from src.DatabaseMethods import get_all_entries, get_entries_by_activity, \
    get_entries_by_dates, get_todays_entry, set_up_db, update_database_to_new_version
from src.Entry import Entry
from src.stats import average_mood_per_activity, average_mood_per_day
from src.util import put_db_back

logger = logging.getLogger('moodli_logger')


def daily_entry(args, **kwargs):
    """Function to vall when daily entry subparser is called.

    Args:
        args (Namespace): Args specified via argparse.
        kwargs(dict): Dict of extra options
    """
    options = parse_config()
    set_up_db(options['database_location'])
    entry = Entry(args.content, args.mood, args.activities, args.hours_of_sleep)
    entry.save_to_database(options['database_location'])
    logger.info(entry)
    put_db_back(options)

def get_entry(args, **kwargs):
    """Function to call when get entry subparser is called.

    Args:
        args (Namespace): Args specified via argparse.
        kwargs(dict): Dict of extra options
    """
    options = parse_config()
    set_up_db(options['database_location'])
    if args.today:
        logger.info('\n'.join(str(x) for x in \
            get_todays_entry(options['database_location'])))
    elif args.activity:
        logger.info('\n'.join(str(x) for x in \
            get_entries_by_activity(args.activity, options['database_location'])))
    elif args.dates:
        logger.info('\n'.join(str(x) for x in \
            get_entries_by_dates(args.dates, options['database_location'])))
    elif args.all:
        logger.info('\n'.join(str(x) for x in \
            get_all_entries(options['database_location'])))
    else:
        logger.error("HMM not sure how you got here")
    put_db_back(options)

def stats(args, **kwargs):
    """Function to call when stats subparser is called.

    Args:
        args (Namespace): Args specified via argparse.
        kwargs(dict): Dict of extra options
    """
    options = parse_config()
    set_up_db(options['database_location'])
    average_mood_per_activity(options['database_location'])
    average_mood_per_day(options['database_location'])
    put_db_back(options)

def update_database(args, **kwargs):
    """Subparser update-database command will call this.

    Args:
        args (Namespace): Args specified via argparse.
        kwargs(dict): Dict of extra options
    """
    options = parse_config()
    set_up_db(options['database_location'])
    update_database_to_new_version(options['database_location'])
    put_db_back(options)

def create_config(args, **kwargs):
    """Subparser create-config will call this

    Args:
        args (Namespace): Args specified via argparse.
        kwargs(dict): Dict of extra options
    """
    write_config_file()

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

def get_parser():
    """Use argparse to define the command line parsers/options

    Returns:
        ArgumentParser: The argument parser for moodli
    """
    parser = argparse.ArgumentParser(description="Command line blog")
    parser.add_argument("--debug", action="store_true", help="Output debug logging")
    subparsers = parser.add_subparsers()

    get_entry_subparser = subparsers.add_parser("get-entry", help="Get a post.",
                                                parents=[parser], add_help=False)
    mutually_exclusive = get_entry_subparser.add_mutually_exclusive_group(required=True)
    mutually_exclusive.add_argument("--today", '-t', action="store_true", help="View todays entry.")
    mutually_exclusive.add_argument("--activity", '-a', type=str,
                                    help="Get all entries that you did an activity")
    mutually_exclusive.add_argument("--dates", '-d', nargs="+",
                                    help="Get all entries on the given dates. Format yyyy-mm-dd")
    mutually_exclusive.add_argument("--all", action="store_true", help="Get all entries")
    get_entry_subparser.set_defaults(func=get_entry)

    daily_entry_subparser = subparsers.add_parser("daily-entry", help="Enter your daily entry",
                                                  parents=[parser], add_help=False)
    daily_entry_subparser.add_argument("--mood", '-m', required=True, type=mood_type,
                                       help="How do you feel out of 10")
    daily_entry_subparser.add_argument("--content", '-n', type=str, default="",
                                       help="A brief journal entry of what you did/how you felt today.")
    daily_entry_subparser.add_argument("--activities", '-a', nargs="+", default=[],
                                       help="List of activities you did today.")
    daily_entry_subparser.add_argument("--hours-of-sleep", '-hos', type=int,
                                       help="How many hours of sleep did you get last night")
    daily_entry_subparser.set_defaults(func=daily_entry)

    stats_parser = subparsers.add_parser("stats", add_help=False,
                                         help="Get stats on what activities make you feel better or worse.",
                                         parents=[parser])
    stats_parser.set_defaults(func=stats)

    update_database_parser = subparsers.add_parser("update-database", parents=[parser], add_help=False,
                                                   help="Update database to new version.")
    update_database_parser.set_defaults(func=update_database)

    create_config_parser = subparsers.add_parser("create-config", parents=[parser], add_help=False,
                                                 help="Create the config file in ~/.moodli/moodli.config")
    create_config_parser.set_defaults(func=create_config)
    return parser
