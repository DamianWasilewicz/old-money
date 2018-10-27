import sqlite3

from passlib.hash import sha256_crypt

def addUserCheck(username, password):
    '''
    Checks if a new user chose a username that already exists in the logins database. If the username can be used, a new login is created, a new user is added to the users database, and returns true.
    '''
    # Opens the logins database
    LOGIN = "./data/logins.db"
    db = sqlite3.connect(LOGIN)
    c = db.cursor()

    # Returns a list of any existing users with the given username. If there is
    # no user with the same name, returns an empty list.
    cmd = "SELECT * FROM info WHERE username = '{}'".format(username)
    check = c.execute(cmd).fetchall()

    # If a user already exists (the list is not empty), return false.
    if check:
        db.commit()
        db.close()
        return False

    # If no user exists (the list is empty), add the user into the database
    # with their encrypted password. Returns true because user is successfully
    # added.
    else:
        # Encrypts password.
        password = sha256_crypt.hash(password)
        info = [[username, password]]
        # Inserts the username and encrypted password into the info table.
        c.executemany('INSERT INTO info VALUES (?, ?)', info)

        db.commit()
        db.close()
        return True

def listLogins():
    '''Returns a list of all logins in the logins database.'''
    # Opens logins database
    LOGIN = "./data/logins.db"
    db = sqlite3.connect(LOGIN)
    c = db.cursor()

    # Returns a list of all usernames and hashed passwords.
    cmd = "SELECT * FROM info"   # Selecting with WHERE may give errors.
    list = c.execute(cmd).fetchall()

    db.commit()
    db.close()

    return list
