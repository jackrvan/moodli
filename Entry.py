from datetime import datetime

from constants import dbopen, MOODS_DB

class Entry():
    def __init__(self, content, mood, activities, date=datetime.now().date()):
        self.content = content
        self.mood = mood
        self.activities = activities
        self.date = date
    
    def __str__(self):
        activities = ', '.join(self.activities)
        return f'================\nDate: {self.date}\nMood: {self.mood}/10\nActivities: {activities}\nDiary Entry: {self.content}\n================'

    def save_to_database(self):
        with dbopen(MOODS_DB) as db:
            db.execute("INSERT INTO entries(content, mood, date) VALUES(?, ?, ?)", (self.content, self.mood, self.date))
            entry_id = db.lastrowid
            for activity in self.activities:
                activity_ids = db.execute("SELECT rowid FROM activities WHERE activity = ?", (activity,)).fetchall()
                if not activity_ids:
                    # We do not have this tag in our db yet
                    db.execute("INSERT INTO activities(activity) VALUES(?)", (activity,))
                    activity_id = db.lastrowid
                elif len(activity_ids) == 1:
                    activity_id = activity_ids[0][0]
                else:
                    print(f"Found more than one activity of {activity}")
                    return
                db.execute("INSERT INTO entry_activities(entry_id, activity_id) VALUES(?, ?)", (entry_id, activity_id))
