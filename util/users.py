import sqlite3

def createUser(user):
    '''Creates a new user entry(table) in the users database.'''
    # Opens the users database.
    USERS = "./data/users.db"
    db = sqlite3.connect(USERS)
    c = db.cursor()

    # Creates a table with the given username.
    cmd = "CREATE TABLE [{}](stories TEXT, timestamp TEXT)".format(user)
    c.execute(cmd)

    db.commit()
    db.close()
    return

def addContent(user, story, timestamp):
    '''
    Creates a new row in the user's contributions table with the story name and timestamp of the contriubtion.
    '''
    # Opens the users database.
    USERS = "./data/users.db"
    db = sqlite3.connect(USERS)
    c = db.cursor()

    # In the user's table, insert the story name and timestamp of contribution.
    cmd = "INSERT INTO [{}] VALUES(?,?)".format(user)
    values = [[story,timestamp]]
    c.executemany(cmd, values)

    db.commit()
    db.close()
    return

def yourContributions(user):
    '''Returns a list of all contributions made by the provided user.'''
    # Opens the users database.
    USERS = "./data/users.db"
    db = sqlite3.connect(USERS)
    c = db.cursor()

    # Returns a list of all stories in the user's table.
    cmd = "SELECT * FROM '{}'".format(user)
    contributions = c.execute(cmd).fetchall()

    db.commit()
    db.close()
    return contributions
