from passlib.hash import sha256_crypt
import sqlite3

LOGIN = "info.db"

db = sqlite3.connect(LOGIN)
c = db.cursor()

c.execute('CREATE TABLE info (username TEXT, password TEXT)')

password = sha256_crypt.hash('password')
info = [['rpeci', password] , ['mzhao3', password] , ['qzhou', password ]]
print(info)

c.executemany('INSERT INTO info VALUES (?, ?)', info)

db.commit()
db.close()
