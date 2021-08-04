import os
import logging
from datetime import datetime
from collections import namedtuple

from src.util import dbopen
from src.constants import ENTRY_COLUMNS
from src.Entry import Entry

# entry.content looks a lot cleaner than entry[1]
EntryTuple = namedtuple("EntryTuple", ['rowid', 'content', 'mood', 'sleep', 'date'])
logger = logging.getLogger('moodli_logger')


def set_up_db(db_path):
    """Create tables in database if they do not exist yet

    Args:
        db_path (str): Path to our database.
    """
    create_entries = "CREATE TABLE IF NOT EXISTS " \
                     "entries(content TEXT, mood INTEGER NOT NULL, sleep INTEGER, date TEXT NOT NULL)"
    create_activities = "CREATE TABLE IF NOT EXISTS activities(activity  TEXT NOT NULL)"
    create_entry_activities = "CREATE TABLE IF NOT EXISTS " \
                              "entry_activities(entry_id INTEGER, activity_id INTEGER, " \
                              "FOREIGN KEY(entry_id) REFERENCES entries(rowid), " \
                              "FOREIGN KEY(activity_id) REFERENCES activities(rowid))"
    create_statements = [create_entries, create_activities, create_entry_activities]
    if not os.path.exists(db_path):
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))
        logger.debug("Writing %s", db_path)
        with dbopen(db_path) as db:
            for create_statement in create_statements:
                db.execute(create_statement)

def get_todays_entry(db_path):
    """Get the entry from today.

    Args:
        db_path (str): Path to our database.

    Returns:
        list(Entry): List of entries that were entered today.
    """
    with dbopen(db_path) as db:
        todays_entries = db.execute("SELECT rowid, content, mood, sleep, date " \
            "FROM entries WHERE date = ?", (datetime.now().date(),)).fetchall()
        entries = []
        if not todays_entries:
            logger.info("You have not added an entry for today yet.")
        elif len(todays_entries) > 1:
            logger.warning("You somehow have more than one entry today.")
            for entry in todays_entries:
                entry = EntryTuple._make(entry)
                activities = get_activities_from_entry_id(entry.rowid, db_path)
                entries.append(Entry(entry.content, entry.mood, activities, entry.sleep, entry.date))
        else:
            entry = EntryTuple._make(todays_entries[0])
            activities = get_activities_from_entry_id(entry.rowid, db_path)
            entries.append(Entry(entry.content, entry.mood, activities, entry.sleep, entry.date))
    return entries

def get_entries_by_activity(activity, db_path):
    """Get all entries that we did an activity.

    Args:
        activity (str): Activity we want to search for.
        db_path (str): Path to our database.

    Returns:
        list(Entry): List of entries that we did this activity.
    """
    entries = []
    with dbopen(db_path) as db:
        get_entries_query = """SELECT entry_id, content, mood, sleep, date FROM 'entries'
                               INNER JOIN entry_activities ON entries.rowid = entry_activities.entry_id 
                               INNER JOIN activities ON activity_id = activities.rowid
                               WHERE activity = '{}'
                            """.format(activity)
        for entry in db.execute(get_entries_query).fetchall():
            entry = EntryTuple._make(entry)
            activities = get_activities_from_entry_id(entry.rowid, db_path)
            entries.append(Entry(entry.content, entry.mood, activities, entry.sleep, entry.date))
    return entries

def get_entries_by_dates(dates, db_path):
    """Get all entries that were posted on a date in dates

    Args:
        dates (list(str)): List of dates in format yyyy-mm-dd.
        db_path (str): Path to our database.

    Returns:
        list(Entry): List of entries posted on a date in dates.
    """
    entries = []
    with dbopen(db_path) as db:
        for date in dates:
            get_entries_query = "SELECT rowid, content, mood, sleep, date FROM 'entries' WHERE date = '{}'" \
                                .format(date.strip())
            for entry in db.execute(get_entries_query).fetchall():
                entry = EntryTuple._make(entry)
                activities = get_activities_from_entry_id(entry[0], db_path)
                entries.append(Entry(entry.content, entry.mood, activities, entry.sleep, entry.date))
    return entries

def get_activities_from_entry_id(entry_id, db_path):
    """Get all activities with entry id entry_id.

    Args:
        entry_id (int): entry_id of the entry we want to find.
        db_path (str): Path to our database.

    Returns:
        list(str): List of activities we did on the specified entry.
    """
    with dbopen(db_path) as db:
        activities = [x[0] for x in db.execute("SELECT activity FROM entry_activities " \
            "INNER JOIN activities ON entry_activities.activity_id = activities.rowid " \
                "WHERE entry_id=?", (entry_id,)).fetchall()]
        return activities

def get_all_entries(db_path):
    """Get all entries from our database

    Args:
        db_path (str): Path to our database.

    Returns:
        list(Entry): List of all entries found in our database.
    """
    logger.debug("Accessing DB %s", db_path)
    with dbopen(db_path) as db:
        entries = []
        for entry in db.execute("SELECT rowid, content, mood, sleep, date FROM entries").fetchall():
            entry = EntryTuple._make(entry)
            activities = get_activities_from_entry_id(entry[0], db_path)
            entries.append(Entry(entry.content, entry.mood, activities, entry.sleep, entry.date))
        return entries

def update_database_to_new_version(db_path):
    """Update our database to the latest version.
    Will just add any missing columns to our database.

    Args:
        db_path (str): Path to our database.
    """
    with dbopen(db_path) as db:
        missing_columns = set(ENTRY_COLUMNS.keys()) - \
                            {x[1] for x in db.execute("PRAGMA table_info(entries)").fetchall()}
        for column_name in missing_columns:
            db.execute("ALTER TABLE entries ADD {} {}".format(column_name, ENTRY_COLUMNS[column_name]))

def delete_from_database(db_path, date):
    with dbopen(db_path) as db:
        db.execute(f"DELETE FROM entries WHERE date = '{date}'")
        print(f"Deleted {db.rowcount} entries")

