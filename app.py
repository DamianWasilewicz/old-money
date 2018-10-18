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
    DB_FILE="logins.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor() #facilitate db ops
    usrn = request.form['username']
    passw= request.form['password']
    print (usrn, passw)
    cmd = """SELECT * FROM info""" #selecting with WHERE may give errors
    threadC = c.execute(cmd).fetchall()
    
    for entry in threadC: 
        if (entry[0] == usrn):
            print(entry[1])
            print(sha256_crypt.hash(passw))
            if sha256_crypt.verify(passw, entry[1]):
                return "SUCCESS!!"
            return "NAY PASSWORD"
    return "no such username"


if __name__ == "__main__":
    app.debug = True
    app.run()
