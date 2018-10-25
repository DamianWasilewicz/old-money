import sqlite3, os

import time, datetime

from flask import Flask, render_template, request, session, redirect, url_for, flash

from passlib.hash import sha256_crypt

from util import dbUpdate, all_stories,users, stories

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route("/")
def root():
    if 'username' in session:
        return render_template("home.html", username = session['username'])
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
                return redirect("/")
            flash("NAY PASSWORD")
            return redirect("/")

    flash("username " + usrn + " not found. please try again")
    db.commit()
    db.close()

    return redirect("/")

@app.route("/display")
def display():
    'displays one story selected in entirety'
    if 'username' not in session:
        flash("You have been logged out.")
        return redirect("/")

    nm = request.args.get("story")
    if nm == None:
        flash("no valid input error")
        return redirect("/")
    DB_FILE = "data/stories.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops

    if not stories.hathContributed(session['username'], nm):
        db.commit()
        db.close()
        return redirect("/editPage?story="+nm)

    cmd = """SELECT contribution FROM """ + nm
    contributions = c.execute(cmd).fetchall()
    s = ""
    # should probably display author / timestamp of last contributions
    for txt in contributions:
        s += txt[0] + " "
    db.commit()
    db.close()

    return render_template("viewStory.html", title = nm, content = s)

@app.route("/editPage")#edit stories
def editPage():
    if 'username' not in session:
        flash("You have logged out.")
        return redirect("/")
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
    session['storyname']=nm
    return render_template("editStory.html", title = nm, content = lastC)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    flash("You have been successfully logged out.")
    return redirect("/")

@app.route('/addStory', methods = ["POST"])
def parse_submission():
    'allows users to add an update to the story'
    if 'username' not in session:
        flash("You have been logged out.")
        return redirect("/")

    content = request.form["content"]
    stnm = session['storyname']

    #print (test)
    if not content:# makes sure content is not empty

        flash("Please add Content.")#this flash does not show

        session.pop('storyname')
        return redirect("/editPage?story="+stnm)
    usern = session['username']
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    dbUpdate.addStories(usern, stnm, content)
    session.pop('storyname')
    return render_template('success.html', title = stnm, time = st)

@app.route('/newStory', methods = ['POST', 'GET'])
def newStoryPage():
    'returns page to add a new story'
    if 'username' not in session:
        flash("You have been logged out.")
        return redirect("/")

    if (request.method == 'GET'):
        return render_template("addStory.html")
    else:
        return addNewStory()

def addNewStory():
    'method to take user input for new story and add to database'
    Title = request.form['title'] #uppercase to disambiguate from template
    contribution = request.form['contribution']

    # checks if there is a title
    if not Title:
        flash("Please enter a title!")
        return redirect("/newStory")
    # checks if there is content
    if not contribution:
        flash("Put some words in that story!")
        return redirect("/newStory")

    # if there is a title and content

    if stories.newStory(Title):
        dbUpdate.addStories(session['username'], Title, contribution)

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return render_template('success.html', title = Title, time = st)

    flash("This story ("+ Title+ ") has already been created. Please create another story.")
    return redirect("/newStory")

@app.route("/viewYourStories", methods = ['GET','POST'])
def yourStories():
    """display a list of your stories"""
    if 'username' not in session:
        flash("You have been logged out.")
        return redirect("/")

    return render_template("allStories.html",
                            specifier = "you've contributed to",
                            content = users.yourContributions(session['username']) )



@app.route('/register', methods = ['POST', 'GET'])
def register():
    # if the 'create user' button is pressed, the method is GET
    # loads the page to create a user
    if request.method == 'GET':
        return render_template("createUser.html")

    # if the 'submit' button is pressed, the method is POST
    # sends the information
    else:
        return addUser()

def addUser():
    # takes user-inputted data
    usrn = request.form["username"]
    pass1 = request.form["password1"]
    pass2 = request.form["password2"]

    # should checks be added for empty user/passw
    # users that are already in the system

    # works even if password field is empty
    # first checks if passwords are matching
    if (pass1 == pass2):
        # success stores the boolean from users.py
        # is the user successfully added to the database? (the username is not already taken)
        success = users.addUser(usrn, pass1)

        # if successfully added
        if success:
            # success message
            flash( "User " + usrn + " created. Please log in.")
            # return to the landing site to log in again
            return redirect("/")

        # username was already taken.
        else:
            flash("Username " + usrn+ " is already taken. please try again")
            return redirect("/register")

    # passwords do not match
    flash ("Your passwords do not match. Please reenter your password")
    return redirect ("/register")

# gets a list of all tables in a database
@app.route("/viewAllStories")
def listAll():
    DB_FILE = "data/stories.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops
    stories = c.execute('SELECT name FROM sqlite_master WHERE type = "table" ').fetchall()
    db.commit()
    db.close()
    return render_template("allStories.html", specifier = "in our collection", content = stories)


if __name__ == "__main__":
    app.debug = True
    app.run()
