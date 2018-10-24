from flask import Flask, request
import time, datetime
import sqlite3
from util import users

def addStories(usern, storyName, contrib):
    storyName = storyName.replace(" ", "_")
    DB_FILE = "./data/stories.db"#database file opens from app.py directory
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops
    cmd = "INSERT INTO {} VALUES(?,?,?)".format(storyName)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    vals= [[(usern), (st), (contrib)]]
    c.executemany(cmd, vals)
    db.commit()
    db.close()
    users.addContent(usern, storyName, st)#make update in users.db
    return

#addStories("qzhou", "Frankenstein","who made him?")
#addStories("rpeci", "Frankenstein", "This was a question that no one could answer")
