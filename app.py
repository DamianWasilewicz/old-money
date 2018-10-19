from flask import Flask, render_template, request, session
import sqlite3
from passlib.hash import sha256_crypt

DB_FILE="logins.db"
#-----------------??? useful???-----------------
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor() #facilitate db ops
app = Flask(__name__)
#----------------???---------------
@app.route("/")
def root():
    return render_template("login.html")

@app.route("/auth", methods = ["POST"])
def check():
    DB_FILE="data/logins.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops
    usrn = request.form['username']
    passw= request.form['password']
    #print (usrn, passw)
    cmd = """SELECT * FROM info""" #selecting with WHERE may give errors
    threadC = c.execute(cmd).fetchall()
    
    for entry in threadC: 
        if (entry[0] == usrn):
            print(entry[1])
            print(sha256_crypt.hash(passw))
            if sha256_crypt.verify(passw, entry[1]):
                
                return '''SUCCESS!!\n<a href="/display?story=Frankenstein">view stories</a>\n<a href="/editPage?story=Frankenstein">edit stories</a>'''
            return "NAY PASSWORD"
    return "no such username"

@app.route("/display")#displays one story selected in entirety
def display():
    DB_FILE = "data/stories.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops
    nm = request.args.get("story")
    cmd = """SELECT contribution FROM """ + nm
    contributions = c.execute(cmd).fetchall()
    s = nm+"\n"
    for txt in contributions:
        s += txt[0]+" "
    return s

@app.route("/editPage")#edit stories
def editPage():
    DB_FILE = "data/stories.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops
    nm = request.args.get("story")
    # don't know how to select last addition
    cmd = """SELECT * FROM """+nm
    lastC =""
    contributions = c.execute(cmd).fetchall()
    lastC = contributions[len(contributions)-1][2]
    return render_template("story.html", title = nm, content = lastC)

if __name__ == "__main__":
    app.debug = True
    app.run()
