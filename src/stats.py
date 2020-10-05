from tabulate import tabulate
from collections import defaultdict
from datetime import datetime

from constants import dbopen, MOODS_DB

def average_mood_per_activity():
    with dbopen(MOODS_DB) as db:
        all_activities = db.execute("SELECT activity FROM activities").fetchall() 
        activity_to_list_of_moods = {}  # Dict of activity that maps to a list of moods out of 10
        for activity in all_activities:
            entry_ids = db.execute("""SELECT entry_id FROM entry_activities 
                                      INNER JOIN activities ON entry_activities.activity_id = activities.rowid 
                                      WHERE activity='{}'""".format(activity[0])).fetchall()
            activity_to_list_of_moods[activity[0]] = [db.execute("SELECT mood FROM entries WHERE rowid = {}".format(entry_id[0])).fetchall()[0][0] for entry_id in entry_ids]
        avgs = {}
        for activity, moods in activity_to_list_of_moods.items():
            avgs[activity] = sum(moods)/len(moods)
        print("\nAVERAGE MOOD BY ACTIVITY")
        print(tabulate(sorted(avgs.items(), key=lambda x: x[1], reverse=True), headers=["Activity", "Avg Mood"]))

def average_mood_per_day():
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    with dbopen(MOODS_DB) as db:
        day_to_list_of_moods = defaultdict(list)
        for entry in db.execute("SELECT mood, date FROM entries").fetchall():
            # By default datetime.weekday() has 0 = monday so to have 0 = sunday we add 1 and modulo 7
            day_to_list_of_moods[days[datetime.strptime(entry[1], "%Y-%m-%d").weekday()+1%7]].append(entry[0])
        avgs = {}
        for day, moods in day_to_list_of_moods.items():
            avgs[day] = sum(moods)/len(moods)
        print("\nAVERAGE MOOD BY DAY OF WEEK")
        print(tabulate(avgs.items(), headers=["Day", "Avg Mood"]))