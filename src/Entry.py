import logging
from datetime import datetime

from src.util import dbopen

logger = logging.getLogger('moodli_logger')

class Entry():
    def __init__(self, content, mood, activities, sleep, date=datetime.now().date()):
        self.content = content
        self.mood = mood
        self.activities = activities
        self.date = date
        self.sleep = sleep

    def __str__(self):
        activities = ', '.join(self.activities)
        return '================\n' \
               f'Date: {self.date}\n' \
               f'Mood: {self.mood}/10\n' \
               f'Hours of Sleep: {self.sleep}\n' \
               f'Activities: {activities}\nDiary Entry: {self.content}\n' \
               '================'

    def save_to_database(self, db_path):
        """Save this object to the database

        Args:
            db_path (str): Path to our database.
        Return:
            bool: True if we added to database
        """
        with dbopen(db_path) as db:
            if db.execute("SELECT * FROM ENTRIES WHERE date=?", (self.date,)).fetchall():
                ans = input(f"You already have an entry for {self.date}. Do you want to replace it [y/n]? ")
                if ans not in ['y', 'Y']:
                    print("Not adding new entry")
                    return False
                db.execute("DELETE FROM ENTRIES WHERE date=?", (self.date,))
            db.execute("INSERT INTO entries(content, mood, sleep, date) " \
                "VALUES(?, ?, ?, ?)", (self.content, self.mood, self.sleep, self.date))
            entry_id = db.lastrowid
            for activity in self.activities:
                activity_ids = db.execute("SELECT rowid FROM activities WHERE activity = ?",
                                          (activity,)).fetchall()
                if not activity_ids:
                    # We do not have this tag in our db yet
                    db.execute("INSERT INTO activities(activity) VALUES(?)", (activity,))
                    activity_id = db.lastrowid
                elif len(activity_ids) == 1:
                    activity_id = activity_ids[0][0]
                else:
                    logger.warning("Found more than one activity of %s", activity)
                    return
                db.execute("INSERT INTO entry_activities(entry_id, activity_id) VALUES(?, ?)",
                           (entry_id, activity_id))
        return True
