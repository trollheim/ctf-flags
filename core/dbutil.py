import sqlite3


FILENAME = "database.db"
USER_COUNT = 1000




conn = sqlite3.connect(FILENAME)
conn.execute("CREATE TABLE IF NOT EXISTS tblusers (id integer PRIMARY KEY AUTOINCREMENT, uname text, passwd text);")
conn.execute("CREATE TABLE IF NOT EXISTS tblflags (id integer PRIMARY KEY AUTOINCREMENT, chalenge text, flag text);")
conn.execute("CREATE TABLE IF NOT EXISTS tblflagsusers(flagid integer,userid integer, FOREIGN KEY(userid) REFERENCES tblusers(id), FOREIGN KEY(flagid) REFERENCES tblflags(id) );")

# for i in range(USER_COUNT):
#     names = male
#     if random.randint(0,10) % 2 == 0:
#         names = female
#     fname = names[random.randint(1,len(names))-1]
#     lname = surnames[random.randint(1,len(surnames))-1]
#     credits = random.randint(0,1000)
#     print( " "+fname +" "+lname+" ")
#     print(conn.execute('''INSERT INTO tblusers (id, fname, sname, credits) VALUES (?, ?,?,?)''',(i+1,fname,lname,credits)))



conn.commit()
conn.close()