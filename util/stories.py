from passlib.hash import sha256_crypt
import sqlite3
import time
import datetime
"""
STORIES = "stories.db"

db = sqlite3.connect(STORIES)
c = db.cursor()

c.execute('CREATE TABLE Frankenstein (authors TEXT, timestamp TEXT, contribution TEXT)')

parent_list = []

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print(st)
parent_list.append(['rpeci', st, 'Once upon a time, there was a'])

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print(st)
parent_list.append(['mzhao3', st, 'big scary monster.'])

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print(st)
parent_list.append(['qzhou', st, 'He was very big and scary!'])

c.executemany('INSERT INTO Frankenstein VALUES (?, ?, ?)', parent_list)

db.commit()
db.close()
"""

def newStory(storyName):
    storyName = storyName.replace(" ", "_")
    STORIES = "./data/stories.db"

    db = sqlite3.connect(STORIES)
    c = db.cursor()
    cmd = 'CREATE TABLE {} (authors TEXT, timestamp TEXT, contribution TEXT)'.format(storyName)
    c.execute(cmd)
    return

def hathContributed(username, storyname):
    STORIES = "./data/stories.db"
    db = sqlite3.connect(STORIES)
    c = db.cursor()
    
    cmd = 'SELECT * FROM {} WHERE authors = "{}"'.format(storyname, username)
    result = c.execute(cmd).fetchall()
    if len(result) > 0:
        return True
    return False
#print(hathContributed('qzhou', 'Frankenstein'))
#print(hathContributed('qzhou1', 'Frankenstein'))
