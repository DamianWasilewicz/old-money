from flask import Flask, request,session
import sqlite3


#unchecked, unran, 
DB_FILE="info.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor() #facilitate db ops
app = Flask(__name__)

@app.route("/")
def base(): #just to check
    return """<!DOCTYPE html>
<html>
  <head><title>
      {% block title %}
      {% endblock %}
  </title></head>
  <body>
    {% block content %}
        <form action = "/check">
<input type = "text" name = "username">
<input type = "text" name = "password">
<input type = "submit name = "sub">
</form>
    {% endblock %}

    {% block footer %}

    {% endblock %}
  </body>
</html>"""


@app.route("/check")
def check():
    usrn = request.form['username']
    passw= request.form['password']
    cmd = """SELECT username, password FROM info 
WHERE username = ?, password = ?"""
    matches = c.execute(cmd, [usern,passw]).fetchall()
    return len(matches) ==1


        

    
