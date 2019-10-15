import sqlite3
import csv
import hashlib
import binascii
import os


FILENAME = "database.db"
USER_COUNT = 1000


def hashpass(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

conn = sqlite3.connect(FILENAME)
conn.execute("CREATE TABLE IF NOT EXISTS tblusers (id integer PRIMARY KEY AUTOINCREMENT, uname text UNIQUE, passwd text,sessionkey text);")
conn.execute("CREATE TABLE IF NOT EXISTS tblflags (id integer PRIMARY KEY AUTOINCREMENT, chalenge text, flag text);")
conn.execute("CREATE TABLE IF NOT EXISTS tblflagsusers(flagid integer,userid integer,submmission integer, FOREIGN KEY(userid) REFERENCES tblusers(id), FOREIGN KEY(flagid) REFERENCES tblflags(id) );")

users = []
with open('users.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=':')
    for row in csv_reader:
        users.append((row[0], hashpass(row[1])))
conn.executemany('INSERT INTO tblusers (uname, passwd) VALUES (?,?)', users)

flags = []
with open('flags.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=':')
    for row in csv_reader:
        flags.append((row[0], row[1]))
conn.executemany('INSERT INTO tblflags(chalenge, flag) VALUES (?,?)', flags)



conn.commit()
conn.close()