from datetime import datetime

from constants import dbopen, MOODS_DB

class Entry():
    def __init__(self, content, moods, activities, date=datetime.now().date()):
        self.content = content
        self.moods = moods
        self.activities = activities
        self.date = date
    
    def __str__(self):
        moods = ', '.join(self.moods)
        activities = ', '.join(self.activities)
        return f'================\nDate: {self.date}\nMoods: {moods}\nActivities: {activities}\nDiary Entry: {self.content}\n================'

    def save_to_database(self):
        with dbopen(MOODS_DB) as db:
            db.execute("INSERT INTO entries(content, date) VALUES(?, ?)", (self.content, self.date))
            entry_id = db.lastrowid
            for mood in self.moods:
                mood_ids = db.execute("SELECT rowid FROM moods WHERE mood = ?", (mood,)).fetchall()
                if not mood_ids:
                    # We do not have this tag in our db yet
                    db.execute("INSERT INTO moods(mood) VALUES(?)", (mood,))
                    mood_id = db.lastrowid
                elif len(mood_ids) == 1:
                    mood_id = mood_ids[0][0]
                else:
                    print(f"Found more than one mood of {mood}")
                    return
                db.execute("INSERT INTO entry_moods(entry_id, mood_id) VALUES(?, ?)", (entry_id, mood_id))

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
