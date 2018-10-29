import sqlite3
import os
import time
import datetime

from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, session, redirect, url_for, flash

from util import logins, users, stories

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route("/")
def root():
    '''Landing page.'''
    # If the user is logged in, they are redirected to the home page.
    if 'username' in session:
        return render_template("home.html", username = session['username'])
    return render_template("login.html")


@app.route("/auth", methods = ["POST"])
def check():
    '''Checks if the user is logged in.'''
    usrn = request.form['username']
    passw = request.form['password']

    # Checks if the inputted username and password is in the list of all
    # usernames and hashed passwords.
    threadC = logins.listLogins()
    for entry in threadC:
        # If the username and password match one in the list, a new session is
        # created.
        if (entry[0] == usrn):
            if sha256_crypt.verify(passw, entry[1]):
                session['username'] = usrn
                return redirect("/")
            # If the username matches but the password does not, flash a message
            # for the wrong password.
            flash("NAY PASSWORD")
            return redirect("/")

    # Flashes an error message for no existing username.
    flash("username " + usrn + " not found. please try again")
    return redirect("/")

@app.route("/display")
def display():
    '''Displays one story in it's entirety.'''
    # Checks if the user is logged in. If not, they are redirected to the login
    # page.
    if 'username' not in session:
        flash("You have been logged out.")
        return redirect("/")

    # Checks if there is story selected. If not, user is redirected to the home
    # page.
    nm = request.args.get("story")
    if not nm:
        flash("no valid input error")
        return redirect("/")

    # If there is a story, checks if the user has already contributed to the
    # story. If they have not contributed yet, load page to edit the story.
    if not stories.hasContributed(session['username'], nm):
        return redirect("/editPage?story="+nm)

    # If the user *has* already contributed, load page to view the story.
    return render_template("viewStory.html", title = nm,
                            content = stories.displayStory(nm))

@app.route("/editPage")
def editPage():
    '''Loads page displaying the last contribution to the story and a text box
    for new contributions.
    '''
    # Checks if the user is logged in. If not, they are redirected to the login
    # page.
    if 'username' not in session:
        flash("You have logged out.")
        return redirect("/")

    name = request.args.get("story")
    session["storyname"] = name
    # Retrieves a list containing last contribution to the selected story and
    # the author and time stamp of the last contribution.
    content = stories.lastEdit(name)[0]

    # Returns the page to edit the story.
    return render_template("editStory.html", title = name,
                            contribution = content[2], user = content[0],
                            timestamp = content[1]
                            )

@app.route('/logout')
def logout():
    '''Allows user to logout.'''
    # Removes user from session.
    if 'username' in session:
        session.pop('username')
    flash("You have been successfully logged out.")
    # Redirects user to the landing page.
    return redirect("/")

@app.route('/addStory', methods = ["POST"])
def parse_submission():
    '''Allows users to add an update to the story.'''
    # Checks if the user is logged in. If not, they are redirected to the login
    # page.
    if 'username' not in session:
        flash("You have been logged out.")
        return redirect("/")

    content = request.form["content"]
    stnm = session['storyname']

    # If the content field is empty (there is no content)
    if not content:
        session.pop('storyname')
        # Flashes error message
        flash("Please add Content.")
        return redirect("/editPage?story="+stnm)

    usern = session['username']
    # Creates timestamp.
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # Adds update to the stories database.
    stories.addStories(usern, stnm, content)
    # Adds update to the users database.
    users.addContent(usern, stnm, st)
    session.pop('storyname')
    # Loads the success page since story was successfully contributed to.
    return render_template('success.html', title = stnm, time = st)

@app.route('/newStory', methods = ['POST', 'GET'])
def newStoryPage():
    '''Allows user to create a new story.'''
    # Checks if the user is logged in. If not, they are redirected to the login
    # page.
    if 'username' not in session:
        flash("You have been logged out.")
        return redirect("/")

    # If the 'add story' button is pressed, the method is GET.
    # The page to create a story is loaded.
    if (request.method == 'GET'):
        return render_template("addStory.html")
    # If the 'submit' button for new stories is pressed, the method is POST
    # Adds story to the database.
    else:
        return addNewStory()

def addNewStory():
    '''Takes user input for a new story and add the new story to the stories
    database.
    '''
    storyName = request.form['title']
    contribution = request.form['contribution']

    # Checks if there is a title.
    if not storyName:
        # Flashes error message to input a title.
        flash("Please enter a title!")
        return redirect("/newStory")
    # Checks if there is content.
    if not contribution:
        # Flashes error message to input content.
        flash("Put some words in that story!")
        return redirect("/newStory")

    # Replaces all spaces in the title with underscores.
    storyName = storyName.replace(" ", "_")
    # If the user has provided both title and content, and the story is
    # succesfully added, render the success page.
    if stories.newStory(storyName):
        # Creates timestamp.
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        # Adds story to the stories database.
        stories.addStories(session['username'], storyName, contribution)
        # Adds story to the list of user contributions
        users.addContent(session['username'], storyName, st)
        # Loads the success page since story was successfully added.
        return render_template('success.html', title = storyName, time = st)

    # Flashes error message that the story already exists in the system.
    flash("This story (" + storyName + ") has already been created. Please create another story.")
    return redirect("/newStory")

@app.route("/viewYourStories", methods = ['GET','POST'])
def yourStories():
    '''Displays a list of all stories that the user has contributed to.'''
    # Checks if the user is logged in. If not, they are redirected to the login
    # page.
    if 'username' not in session:
        flash("You have been logged out.")
        return redirect("/")

    # Loads page with a list of links to all the stories the user has
    # contributed to.
    return render_template("allStories.html",
                            specifier = "you've contributed to",
                            content = users.yourContributions(session['username']) )


@app.route('/register', methods = ['POST', 'GET'])
def register():
    '''Allows an unregistered user to create a user and access stories.'''
    # If the 'create user' button is pressed, the method is GET.
    # The page to create a user is loaded.
    if request.method == 'GET':
        return render_template("createUser.html")

    # If the 'submit' button is pressed from the createUser page, the method is
    # POST
    # Checks if user can be successfully added.
    else:
        return addUser()

def addUser():
    '''Checks if the user has inputted matching passwords, and if the username
    does not already exist. If so, the new user is added to the logins and user
    databases.
    '''
    # Stores the user's form data.
    usrn = request.form["username"]
    pass1 = request.form["password1"]
    pass2 = request.form["password2"]

    # Checks if the passwords are matching.
    if (pass1 == pass2):
        # success stores the boolean from users.py
        # is the user successfully added to the database? (the username is not
        # already taken)
        success = logins.addUserCheck(usrn, pass1)

        # if successfully added
        if success:
            # Adds user into the user database.
            users.createUser(usrn)
            # Flash a success message.
            flash( "User " + usrn + " created. Please log in.")
            # Return to the landing site to log in.
            return redirect("/")

        # Flashes error message that the username is already in the system.
        else:
            flash("Username " + usrn + " is already taken. please try again")
            return redirect("/register")

    # Flashes error message that the passwords do not match.
    flash ("Your passwords do not match. Please reenter your password")
    return redirect ("/register")

@app.route("/viewAllStories")
def listAll():
    '''Returns a list of all the stories in the stories database.'''
    # Loads page with a list of links to all the stories in our collection.
    return render_template("allStories.html",
                            specifier = "in our collection",
                            content = stories.allStories()
                            )

if __name__ == "__main__":
    app.debug = False
    app.run()
