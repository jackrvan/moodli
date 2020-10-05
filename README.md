# Command line mood tracker.

## Installation
        git clone https://github.com/jackrvan/moodli.git
        cd moodli
        python setup.py install --user

## Usage
##### - Create your daily entry
        - moodli daily-entry --content \
        "Today was overall a good day. Couldnt do everything I wanted to because Robert stopped by." \
         --mood 8 \
         --activities work tv programming hockey
##### - View your entry from today
        - moodli get-entry --today
##### - View your entries from October 28 1996 and September 26 2020
        - moodli get-entry --dates 1996-10-28 2020-09-26
##### - View all days where you played hockey
        - moodli get-entry --activity hockey