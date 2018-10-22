from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3, os
import time, datetime
from passlib.hash import sha256_crypt

from util import all_stories, dbUpdate

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route("/")
def root():
    if 'username' in session:
        #return redirect("/auth")
        return render_template("home.html", username = session['username'])
    #else:
    #return redirect('/auth')
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


                session['username'] = usrn
                #print(session)
                return '''SUCCESS!!\n<a href="/display?story=Frankenstein">view stories</a>\n<a href="/editPage?story=Frankenstein">edit stories</a>'''
            #return "NAY PASSWORD"
            flash("NAY PASSWORD")
            return redirect("/")

    flash("username " + usrn + " not found. please try again")
    db.commit()
    db.close()

    return redirect("/")
    ##return "no such username"

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
    db.commit()
    db.close()

    return render_template("story.html", title = nm, content = s)

@app.route("/editPage")#edit stories
def editPage():
    DB_FILE = "data/stories.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops
    nm = request.args.get("story")
    session["storyname"] = nm
    # don't know how to select last addition
    cmd = """SELECT * FROM """+nm
    lastC =""
    contributions = c.execute(cmd).fetchall()
    lastC = contributions[len(contributions)-1][2]
    db.commit()
    db.close()

    return render_template("editStory.html", title = nm, content = lastC)

@app.route('/success', methods=['GET', 'POST'])
def parse_submission():
    content = request.form.get("contribution")
    print(content)
    DB_FILE = "data/stories.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops

    nm = request.args.get("story")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    values = [[session['username'], (st), content]]
    print(values)
    cmd = 'INSERT INTO {} VALUES(?,?,?)'.format(nm)
    c.executemany(cmd, values)
    db.commit()
    db.close()

    return render_template('success.html', title = nm, time = st)

@app.route('/logout')
def logout():
    session.pop('username')
    flash("You have been successfully logged out.")
    return redirect("/")

@app.route('/addStory', methods = ["POST"])
def addStory():
    content = request.form["content"]
    dbUpdate.addStories(session['username'], session['storyname'], content)
    session.pop('storyname')
    return "wowie"

@app.route('/register')
def loadPage():
    return render_template("createUser.html")
#add fxn to add users to database

if __name__ == "__main__":
    app.debug = True
    app.run()
