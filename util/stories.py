import sqlite3
import time
import datetime

from passlib.hash import sha256_crypt


def newStory(storyName):
    """adds a new story"""
    storyName = storyName.replace(" ", "_")
    STORIES = "./data/stories.db"

    db = sqlite3.connect(STORIES)
    c = db.cursor()

    check = c.execute('SELECT name FROM sqlite_master WHERE name = "{}"'.format(storyName)).fetchall()
    print(check)
    if check:
        db.commit()
        db.close()
        return False

    cmd = 'CREATE TABLE {} (authors TEXT, timestamp TEXT, contribution TEXT)'.format(storyName)
    c.execute(cmd)

    db.commit()
    db.close()
    return True

def hathContributed(username, storyname):
    """returns true if username has contributed to it, else false"""
    STORIES = "./data/stories.db"
    db = sqlite3.connect(STORIES)
    c = db.cursor()

    cmd = 'SELECT * FROM {} WHERE authors = "{}"'.format(storyname, username)
    result = c.execute(cmd).fetchall()
    if result:
        return True
    return False
#print(hathContributed('qzhou', 'Frankenstein'))
#print(hathContributed('qzhou1', 'Frankenstein'))
