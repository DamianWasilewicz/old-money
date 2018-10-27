import time
import datetime
import sqlite3

def newStory(storyName):
    '''Adds a story to the stories database. Returns true if story is added.'''
    # Opens the stories database
    STORIES = "./data/stories.db"
    db = sqlite3.connect(STORIES)
    c = db.cursor()

    # Returns a list of any existing stories with the given title. If there is
    # no story with the same name, returns an empty list.
    # Selects from sqlite_master because all stories are separate tables.
    cmd = "SELECT name FROM sqlite_master WHERE name = '{}'".format(storyName)
    check = c.execute(cmd).fetchall()

    # If the story already exists (the list is not empty), the story is not
    # added. (Returns false).
    if check:
        db.commit()
        db.close()
        return False

    # Otherwise, the table is created with the given title. (Return true).
    cmd = "CREATE TABLE '{}' (authors TEXT, timestamp TEXT, contribution TEXT)".format(storyName)
    c.execute(cmd)

    db.commit()
    db.close()
    return True

def hasContributed(username, storyname):
    '''Checks if a user has already contributed to a story.'''
    # Opens the stories database
    STORIES = "./data/stories.db"
    db = sqlite3.connect(STORIES)
    c = db.cursor()

    # Returns a list if the user has contributed to the story.
    cmd = "SELECT * FROM '{}' WHERE authors = '{}'".format(storyname, username)
    result = c.execute(cmd).fetchall()
    # If there is a contribution in the list, then the user has contributed to
    # the story. (Return true).
    if result:
        return True
    # Otherwise, the user has not contributed. (Return false).
    return False

def allStories():
    '''Returns a list of all the stories in the database.'''
    # Opens the stories database.
    DB_FILE = "./data/stories.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # Selects from sqlite_master because all stories are separate tables.
    c.execute('SELECT name FROM sqlite_master WHERE type = "table" ')
    stories = c.fetchall()

    db.commit()
    db.close()

    return stories

def addStories(usern, storyName, contrib):
    '''Adds the user's contributions to the appropriate table in the db.'''
    # Opens the stories database.
    STORIES = "./data/stories.db"
    db = sqlite3.connect(STORIES)
    c = db.cursor()

    cmd = "INSERT INTO '{}' VALUES(?,?,?)".format(storyName)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    vals= [[(usern), (st), (contrib)]]
    c.executemany(cmd, vals)

    db.commit()
    db.close()
    return

def lastEdit(name):
    '''Returns the last edit made under a given story.'''
    # Opens the stories database.
    STORIES = "./data/stories.db"
    db = sqlite3.connect(STORIES)
    c = db.cursor()

    # Returns a list (with one tuple) of the entry submitted last.
    # ORDER BY reorders the table by timestamp
    # DESC LIMIT 1 puts the table in descending order, and returns 1 row
    cmd = "SELECT * FROM '{}' ORDER BY timestamp DESC LIMIT 1".format(name)
    lastEdit = c.execute(cmd).fetchall()

    db.commit()
    db.close()
    return lastEdit

def displayStory(name):
    # Opens the stories database.
    STORIES = "./data/stories.db"
    db = sqlite3.connect(STORIES)
    c = db.cursor()

    # Returns a list of all contributions, authors, and timestamps in the table
    # of the provided story.
    cmd = "SELECT * FROM '{}'".format(name)
    contributions = c.execute(cmd).fetchall()

    db.commit()
    db.close()
    return contributions
