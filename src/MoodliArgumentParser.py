import argparse

from src.Entry import Entry
from src.DatabaseMethods import get_todays_entry, get_entries_by_activity, \
    get_entries_by_dates, get_all_entries, update_database_to_new_version
from src.stats import average_mood_per_activity, average_mood_per_day

def daily_entry(args, **kwargs):
    """Function to vall when daily entry subparser is called.

    Args:
        args (Namespace): Args specified via argparse.
        kwargs(dict): Dict of extra options
    """
    entry = Entry(args.content, args.mood, args.activities, args.hours_of_sleep)
    entry.save_to_database(kwargs['db_path'])
    print(entry)

def get_entry(args, **kwargs):
    """Function to call when get entry subparser is called.

    Args:
        args (Namespace): Args specified via argparse.
        kwargs(dict): Dict of extra options
    """
    if args.today:
        print('\n'.join(str(x) for x in get_todays_entry(kwargs['db_path'])))
    elif args.activity:
        print('\n'.join(str(x) for x in get_entries_by_activity(args.activity, kwargs['db_path'])))
    elif args.dates:
        print('\n'.join(str(x) for x in get_entries_by_dates(args.dates, kwargs['db_path'])))
    elif args.all:
        print('\n'.join(str(x) for x in get_all_entries(kwargs['db_path'])))
    else:
        print("HMM not sure how you got here")

def stats(args, **kwargs):
    """Function to call when stats subparser is called.

    Args:
        args (Namespace): Args specified via argparse.
        kwargs(dict): Dict of extra options
    """
    print('type = {}'.format(type(kwargs)))
    average_mood_per_activity(kwargs['db_path'])
    average_mood_per_day(kwargs['db_path'])

def update_database(args, **kwargs):
    """Subparser update-database command will call this.

    Args:
        args (Namespace): Args specified via argparse.
        kwargs(dict): Dict of extra options
    """
    update_database_to_new_version(kwargs['db_path'])

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
    subparsers = parser.add_subparsers()

    get_entry_subparser = subparsers.add_parser("get-entry", help="Get a post.")
    mutually_exclusive = get_entry_subparser.add_mutually_exclusive_group(required=True)
    mutually_exclusive.add_argument("--today", '-t', action="store_true", help="View todays entry.")
    mutually_exclusive.add_argument("--activity", '-a', type=str,
                                    help="Get all entries that you did an activity")
    mutually_exclusive.add_argument("--dates", '-d', nargs="+",
                                    help="Get all entries on the given dates. Format yyyy-mm-dd")
    mutually_exclusive.add_argument("--all", action="store_true", help="Get all entries")
    get_entry_subparser.set_defaults(func=get_entry)

    daily_entry_subparser = subparsers.add_parser("daily-entry", help="Enter your daily entry")
    daily_entry_subparser.add_argument("--mood", '-m', required=True, type=mood_type,
                                       help="How do you feel out of 10")
    daily_entry_subparser.add_argument("--content", '-n', type=str, default="",
                                       help="A brief journal entry of what you did/how you felt today.")
    daily_entry_subparser.add_argument("--activities", '-a', nargs="+", default=[],
                                       help="List of activities you did today.")
    daily_entry_subparser.add_argument("--hours-of-sleep", '-hos', type=int,
                                       help="How many hours of sleep did you get last night")
    daily_entry_subparser.set_defaults(func=daily_entry)

    stats_parser = subparsers.add_parser("stats",
                                         help="Get stats on what activities make you feel better or worse.")
    stats_parser.set_defaults(func=stats)

    update_database_parser = subparsers.add_parser("update-database",
                                                   help="Update database to new version.")
    update_database_parser.set_defaults(func=update_database)
    return parser
