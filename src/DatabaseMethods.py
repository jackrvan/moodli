import os
from datetime import datetime
from collections import namedtuple

from src.ConfigSettings import ConfigSettings
from src.constants import dbopen, ENTRY_COLUMNS
from src.Entry import Entry

# entry.content looks a lot cleaner than entry[1]
EntryTuple = namedtuple("EntryTuple", ['rowid', 'content', 'mood', 'sleep', 'date'])


def set_up_db():
    create_entries = "CREATE TABLE IF NOT EXISTS entries(content TEXT, mood INTEGER NOT NULL, sleep INTEGER, date TEXT NOT NULL)"
    create_activities = "CREATE TABLE IF NOT EXISTS activities(activity  TEXT NOT NULL)"
    create_entry_activities = "CREATE TABLE IF NOT EXISTS entry_activities(entry_id INTEGER, activity_id INTEGER, " \
                              "FOREIGN KEY(entry_id) REFERENCES entries(rowid), " \
                              "FOREIGN KEY(activity_id) REFERENCES activities(rowid))"
    create_statements = [create_entries, create_activities, create_entry_activities]
    if not os.path.exists(ConfigSettings.db_path):
        if not os.path.exists(os.path.dirname(ConfigSettings.db_path)):
            os.makedirs(os.path.dirname(ConfigSettings.db_path))
        print(f"Writing {ConfigSettings.db_path}")
        with dbopen(ConfigSettings.db_path) as db:
            for create_statement in create_statements:
                db.execute(create_statement)

def get_todays_entry():
    with dbopen(ConfigSettings.db_path) as db:
        todays_entries = db.execute("SELECT rowid, content, mood, sleep, date " \
            "FROM entries WHERE date = ?", (datetime.now().date(),)).fetchall()
        entries = []
        if not todays_entries:
            print("You have not added an entry for today yet.")
        elif len(todays_entries) > 1:
            print("You somehow have more than one entry today.")
            for entry in todays_entries:
                entry = EntryTuple._make(entry)
                activities = get_activities_from_entry_id(entry.rowid)
                entries.append(Entry(entry.content, entry.mood, activities, entry.sleep, entry.date))
        else:
            entry = EntryTuple._make(todays_entries[0])
            activities = get_activities_from_entry_id(entry.rowid)
            entries.append(Entry(entry.content, entry.mood, activities, entry.sleep, entry.date))
    return entries

def get_entries_by_activity(activity):
    entries = []
    with dbopen(ConfigSettings.db_path) as db:
        get_entries_query = """SELECT entry_id, content, mood, sleep, date FROM 'entries'
                               INNER JOIN entry_activities ON entries.rowid = entry_activities.entry_id 
                               INNER JOIN activities ON activity_id = activities.rowid
                               WHERE activity = '{}'
                            """.format(activity)
        for entry in db.execute(get_entries_query).fetchall():
            entry = EntryTuple._make(entry)
            activities = get_activities_from_entry_id(entry.rowid) 
            entries.append(Entry(entry.content, entry.mood, activities, entry.sleep, entry.date))
    return entries

def get_entries_by_dates(dates):
    entries = []
    with dbopen(ConfigSettings.db_path) as db:
        for date in dates:
            get_entries_query = "SELECT rowid, content, mood, sleep, date FROM 'entries' WHERE date = '{}'".format(date.strip())
            for entry in db.execute(get_entries_query).fetchall():
                entry = EntryTuple._make(entry)
                activities = get_activities_from_entry_id(entry[0])
                entries.append(Entry(entry.content, entry.mood, activities, entry.sleep, entry.date))
    return entries

def get_activities_from_entry_id(entry_id):
    with dbopen(ConfigSettings.db_path) as db:
        activities = [x[0] for x in db.execute("SELECT activity FROM entry_activities " \
            "INNER JOIN activities ON entry_activities.activity_id = activities.rowid " \
                "WHERE entry_id=?", (entry_id,)).fetchall()]
        return activities

def get_all_entries():
    print("ACCESSING DB {}".format(ConfigSettings.db_path))
    with dbopen(ConfigSettings.db_path) as db:
        entries = []
        for entry in db.execute("SELECT rowid, content, mood, sleep, date FROM entries").fetchall():
            entry = EntryTuple._make(entry)
            activities = get_activities_from_entry_id(entry[0])
            entries.append(Entry(entry.content, entry.mood, activities, entry.sleep, entry.date))
        return entries

def update_database_to_new_version():
    with dbopen(ConfigSettings.db_path) as db:
        missing_columns = set(ENTRY_COLUMNS.keys()) - set([x[1] for x in db.execute("PRAGMA table_info(entries)").fetchall()])
        for column_name in missing_columns:
            db.execute("ALTER TABLE entries ADD {} {}".format(column_name, ENTRY_COLUMNS[column_name]))
