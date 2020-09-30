#!/bin/env python
import os

from ArgumentParser import get_parser
from constants import MOODS_DB, dbopen


def set_up_db():
    create_entries = "CREATE TABLE IF NOT EXISTS entries(content TEXT, date TEXT NOT NULL)"
    create_moods = "CREATE TABLE IF NOT EXISTS moods(mood TEXT NOT NULL)"
    create_activities = "CREATE TABLE IF NOT EXISTS activities(activity  TEXT NOT NULL)"
    create_entry_moods = "CREATE TABLE IF NOT EXISTS entry_moods(entry_id INTEGER, mood_id INTEGER, " \
                         "FOREIGN KEY(entry_id) REFERENCES entries(rowid), " \
                         "FOREIGN KEY(mood_id) REFERENCES moods(rowid))"
    create_entry_activities = "CREATE TABLE IF NOT EXISTS entry_activities(entry_id INTEGER, activity_id INTEGER, " \
                              "FOREIGN KEY(entry_id) REFERENCES entries(rowid), " \
                              "FOREIGN KEY(activity_id) REFERENCES activities(rowid))"
    create_statements = [create_entries, create_moods, create_activities, create_entry_moods, create_entry_activities]
    if not os.path.exists(MOODS_DB):
        print(f"Writing {MOODS_DB}")
        with dbopen(MOODS_DB) as db:
            for create_statement in create_statements:
                db.execute(create_statement)

def main():
    set_up_db()
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()