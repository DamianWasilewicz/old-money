from flask import Flask, request
import time, datetime
import sqlite3

def addStories(usern, storyName, contrib):
    DB_FILE = "stories.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops
    cmd = "INSERT INTO {} VALUES(?,?,?)".format(storyName)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    vals= [(usern), (st), (contrib)]
    c.executemany(cmd, vals)
    return

addStories("qzhou", "Frankenstein","who made him?")
