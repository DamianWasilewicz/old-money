import sqlite3

from passlib.hash import sha256_crypt



def addUser(username, password):
    """creates user with given username and password"""
    
    LOGIN = "./data/logins.db"
    db = sqlite3.connect(LOGIN)
    c = db.cursor()

    # checks to see if there is a row with the given username
    check = c.execute('SELECT * FROM info WHERE username = \"' + username + '\"').fetchall()
    print (check)

    # if the username is taken
    if check:
        return False

    else:
        # password is encrypted
        password = sha256_crypt.hash(password)
        info = [[username, password]]
        c.executemany('INSERT INTO info VALUES (?, ?)', info)

        #print (info)
        db.commit()
        db.close()
        createUser(username)
        return True

"""User.db functionality"""
def createUser(user):
    """makes a new table in user.db"""
    USERS = "./data/users.db"
    db = sqlite3.connect(USERS)
    c = db.cursor()

    cmd = "CREATE TABLE [{}](stories TEXT, timestamp TEXT)".format(user)
    c.execute(cmd)
    db.commit()
    db.close()
    return

#createUser("trial")
def addContent(user,story, timestamp):
    'add content into user.db'
    USERS = "./data/users.db"
    db = sqlite3.connect(USERS)
    c = db.cursor()

    cmd = "INSERT INTO [{}] VALUES(?,?)".format(user)
    values = [[story,timestamp]]
    c.executemany(cmd, values)
    db.commit()
    db.close()
    return
#addContent("trial", "Frankenstein", "troll")
def yourContributions(user):
    """get list of your contributions"""
    USERS = "./data/users.db"
    db = sqlite3.connect(USERS)
    c = db.cursor()

    cmd = "SELECT stories FROM ["+user+"]"
    listS= c.execute(cmd).fetchall()

    return listS
