from datetime import datetime

from constants import dbopen, MOODS_DB
from Entry import Entry

def get_todays_entry():
    with dbopen(MOODS_DB) as db:
        todays_entries = db.execute("SELECT rowid, content, mood, date FROM entries WHERE date = ?", (datetime.now().date(),)).fetchall()
        entries = []
        if not todays_entries:
            print("You have not added an entry for today yet.")
        elif len(todays_entries) > 1:
            print("You somehow have more than one entry today. Not sure how you managed that so congrats I guess?")
            for entry in todays_entries:
                activities = get_activities_from_entry_id(entry[0])
                entries.append(Entry(entry[1], entry[2], activities, entry[3]))
        else:
            activities = get_activities_from_entry_id(todays_entries[0][0])
            entries.append(Entry(todays_entries[0][1], todays_entries[0][2], activities))
    return entries

def get_entries_by_activity(activity):
    entries = []
    with dbopen(MOODS_DB) as db:
        get_entries_query = """SELECT entry_id, content, mood, date FROM 'entries' 
                               INNER JOIN entry_activities ON entries.rowid = entry_activities.entry_id 
                               INNER JOIN activities ON activity_id = activities.rowid
                               WHERE activity = '{}'
                            """.format(activity)
        for entry in db.execute(get_entries_query).fetchall():
            activities = get_activities_from_entry_id(entry[0]) 
            entries.append(Entry(entry[1], entry[2], activities, entry[3]))
    return entries

def get_entries_by_dates(dates):
    entries = []
    with dbopen(MOODS_DB) as db:
        for date in dates:
            get_entries_query = "SELECT rowid, content, mood, date FROM 'entries' WHERE date = '{}'".format(date.strip())
            for entry in db.execute(get_entries_query).fetchall():
                activities = get_activities_from_entry_id(entry[0])
                entries.append(Entry(entry[1], entry[2], activities, entry[3]))
    return entries

def get_activities_from_entry_id(entry_id):
    with dbopen(MOODS_DB) as db:
        activities = [x[0] for x in db.execute("SELECT activity FROM entry_activities INNER JOIN activities ON entry_activities.activity_id = activities.rowid WHERE entry_id=?", (entry_id,)).fetchall()]
        return activities

def get_all_entries():
    with dbopen(MOODS_DB) as db:
        entries = []
        for entry in db.execute("SELECT rowid, content, mood, date FROM entries").fetchall():
            entries.append(Entry(entry[1], entry[2], get_activities_from_entry_id(entry[0]), entry[3]))
        return entries