from passlib.hash import sha256_crypt
import sqlite3


def addUser(username, password):
    LOGIN = "./data/logins.db"
    db = sqlite3.connect(LOGIN)
    c = db.cursor()

    # checks to see if there is a row with the given username
    c.execute('SELECT * FROM info WHERE username = \"' + username + '\"')
    check = c.fetchall()
    #print (check)

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

    cmd = "CREATE TABLE {}(stories TEXT, timestamp TEXT)".format(user)
    c.execute(cmd)
    db.commit()
    db.close()
    return

#createUser("trial")
def addContent(user,story, timestamp):
    """add content into user.db"""
    USERS = "./data/users.db"
    db = sqlite3.connect(USERS)
    c = db.cursor()

    cmd = "INSERT INTO {} VALUES(?,?)".format(user)
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

    cmd = "SELECT stories FROM "+user
    listS= c.execute(cmd).fetchall()
    listR=[]
    for entry in listS:
        listR.append(entry[0])
    #print (listR)
    return listR
