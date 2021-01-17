from datetime import datetime, timedelta

import pytest

from src.constants import dbopen
from src.DatabaseMethods import get_activities_from_entry_id, get_all_entries, get_entries_by_activity, get_entries_by_dates, get_todays_entry, set_up_db


@pytest.fixture
def setup(tmpdir_factory):
    """Setup our database for testing

    Args:
        tmpdir_factory (pytest TmpDirFactory): A tempdir factory that gets automatically deleted

    Returns:
        (str): Path to database
    """
    temp_database = tmpdir_factory.mktemp("data").join("tmp_db.db")
    set_up_db(temp_database)
    with dbopen(temp_database) as db:
        db.execute("INSERT INTO entries(content, mood, sleep, date) VALUES('This is some content', '8', '8', ?)", (datetime.now().date(),))
        db.execute("INSERT INTO entries(content, mood, sleep, date) VALUES('This is some more content', '1', '1', ?)", ((datetime.now() - timedelta(days=1)).date(),))
        db.execute("INSERT INTO entries(content, mood, sleep, date) VALUES('This is some more more content', '10', '10', ?)", ((datetime.now() - timedelta(days=2)).date(),))
        db.execute("INSERT INTO activities(activity) VALUES('hockey')")
        db.execute("INSERT INTO activities(activity) VALUES('football')")
        db.execute("INSERT INTO activities(activity) VALUES('baseball')")
        db.execute("INSERT INTO entry_activities(entry_id, activity_id) VALUES(1, 1)")
        db.execute("INSERT INTO entry_activities(entry_id, activity_id) VALUES(1, 2)")
        db.execute("INSERT INTO entry_activities(entry_id, activity_id) VALUES(2, 3)")
    return temp_database

@pytest.fixture
def setup_no_entries(tmpdir_factory):
    """Setup our database for testing

    Args:
        tmpdir_factory (pytest TmpDirFactory): A tempdir factory that gets automatically deleted

    Returns:
        (str): Path to database
    """
    temp_database = tmpdir_factory.mktemp("data").join("tmp_db.db")
    set_up_db(temp_database)
    return temp_database

def test_get_todays_entry(setup):
    """Test the get todays entry function when we have an entry from today

    Args:
        setup (pytest.fixture): Input is the pytest fixture from above
    """
    expected = ['================\nDate: 2021-01-17\nMood: 8/10\nHours of Sleep: 8\nActivities: hockey, football\nDiary Entry: This is some content\n================']
    assert expected == [str(x) for x in get_todays_entry(setup)]

def test_get_todays_entry_no_entry(setup_no_entries):
    """Test get_todays_entry when we have no entries

    Args:
        setup_no_entries (pytest.fixture): Pytest fixture defined above
    """
    expected = []
    assert expected == get_todays_entry(setup_no_entries)

def test_get_entries_by_activity(setup):
    """Test the get entries by activity function

    Args:
        setup ([type]): [description]
    """
    expected = ['================\nDate: 2021-01-16\nMood: 1/10\nHours of Sleep: 1\nActivities: baseball\nDiary Entry: This is some more content\n================']
    assert expected == [str(x) for x in get_entries_by_activity('baseball', setup)]

def test_get_entries_by_activity_doesnt_exist(setup):
    """Test the get entries by activity function when the activity doesnt exist

    Args:
        setup ([type]): [description]
    """
    expected = []
    assert expected == get_entries_by_activity('not_exist', setup)

def test_get_entries_by_dates(setup):
    """Test getting an entry by date

    Args:
        setup (pytest.fixture): [description]
    """
    expected = ['================\nDate: 2021-01-17\nMood: 8/10\nHours of Sleep: 8\nActivities: hockey, football\nDiary Entry: This is some content\n================',
                '================\nDate: 2021-01-16\nMood: 1/10\nHours of Sleep: 1\nActivities: baseball\nDiary Entry: This is some more content\n================']
    assert expected == [str(x) for x in get_entries_by_dates([str(datetime.now().date()),
                                                              str((datetime.now() - timedelta(days=1)).date())],
                                                            setup)]

def test_get_activities_from_entry_id(setup):
    """Test get_activities_from_entry_id function

    Args:
        setup (pytest.fixture): [description]
    """
    expected = ['hockey', 'football']
    assert expected == get_activities_from_entry_id(1, setup)

def test_get_all_entries(setup):
    """Test get_all_entries function

    Args:
        setup (pytest.fixture): [description]
    """
    expected = ['================\nDate: 2021-01-17\nMood: 8/10\nHours of Sleep: 8\nActivities: hockey, football\nDiary Entry: This is some content\n================',
                '================\nDate: 2021-01-16\nMood: 1/10\nHours of Sleep: 1\nActivities: baseball\nDiary Entry: This is some more content\n================',
                '================\nDate: 2021-01-15\nMood: 10/10\nHours of Sleep: 10\nActivities: \nDiary Entry: This is some more more content\n================']
    assert expected == [str(x) for x in get_all_entries(setup)]
