import sqlite3
import random


FILENAME = "database.db"
USER_COUNT = 1000

female =[]
male = []
surnames = []



f = open("data/femalenames.txt", "r")
for x in f:
  female.append(x.strip())

f = open("data/malenames.txt", "r")
for x in f:
    male.append(x.strip())

f = open("data/surnames.txt", "r")
for x in f:
    surnames.append(x.strip())




conn = sqlite3.connect(FILENAME)
conn.execute("CREATE TABLE IF NOT EXISTS tblusers (id integer PRIMARY KEY, fname text, sname text, credits int);")
conn.execute("CREATE TABLE IF NOT EXISTS tblflag(flag text);")

for i in range(USER_COUNT):
    names = male
    if random.randint(0,10) % 2 == 0:
        names = female
    fname = names[random.randint(1,len(names))-1]
    lname = surnames[random.randint(1,len(surnames))-1]
    credits = random.randint(0,1000)
    print( str(i+1)+" "+fname +" "+lname+" ")
    print(conn.execute('''INSERT INTO tblusers (id, fname, sname, credits) VALUES (?, ?,?,?)''',(i+1,fname,lname,credits)))



conn.commit()
conn.close()