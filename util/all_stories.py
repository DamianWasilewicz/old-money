from flask import Flask, request
import sqlite3

DB_FILE = 'stories.db'
db = sqlite3.connect(DB_FILE)
c = db.cursor()

def print_story(title):
