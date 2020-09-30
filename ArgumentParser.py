import argparse

from Entry import Entry
from DatabaseMethods import get_todays_entry, get_entries_by_activity, get_entries_by_mood, get_entries_by_dates

def daily_entry(args):
    entry = Entry(args.content, args.moods, args.activities)
    entry.save_to_database()
    print(entry)

def get_entry(args):
    if args.today:
        print('\n'.join(str(x) for x in get_todays_entry()))
    elif args.activity:
        print('\n'.join(str(x) for x in get_entries_by_activity(args.activity)))
    elif args.mood:
        print('\n'.join(str(x) for x in get_entries_by_mood(args.mood)))
    elif args.dates:
        print('\n'.join(str(x) for x in get_entries_by_dates(args.dates)))
    else:
        print("HMM not sure how you got here")

def get_parser():
    parser = argparse.ArgumentParser(description="Command line blog")
    subparsers = parser.add_subparsers()
    
    get_entry_subparser = subparsers.add_parser("get-entry", help="get a post.")
    mutually_exclusive = get_entry_subparser.add_mutually_exclusive_group(required=True)
    mutually_exclusive.add_argument("--today", '-t', action="store_true", help="View todays entry.")
    mutually_exclusive.add_argument("--activity", '-a', type=str, help="Get all entries that you did an activity")
    mutually_exclusive.add_argument("--mood", '-m', type=str, help="Get all entries that you felt a mood")
    mutually_exclusive.add_argument("--dates", '-d', nargs="+", help="Get all entries on the given dates. Format yyyy-mm-dd")
    get_entry_subparser.set_defaults(func=get_entry)

    daily_entry_subparser = subparsers.add_parser("daily-entry", help="Enter your daily entry")
    daily_entry_subparser.add_argument("--moods", '-m', required=True, nargs="+")
    daily_entry_subparser.add_argument("--content", '-n', type=str, default="")
    daily_entry_subparser.add_argument("--activities", '-a', nargs="+", default=[])
    daily_entry_subparser.set_defaults(func=daily_entry)
    return parser