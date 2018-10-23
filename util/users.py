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
        password = sha256_crypt.hash('password')
        info = [[username, password]]
        c.executemany('INSERT INTO info VALUES (?, ?)', info)

        #print (info)
        db.commit()
        db.close()
        return True


#c.execute('CREATE TABLE info (username TEXT, password TEXT)')

#password = sha256_crypt.hash('password')
#info = [['rpeci', password] , ['mzhao3', password] , ['qzhou', password ]]
#print(info)

#c.executemany('INSERT INTO info VALUES (?, ?)', info)
