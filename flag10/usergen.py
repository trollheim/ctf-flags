import random
import hashlib

USER_COUNT = 1000

female =[]
male = []
surnames = []
passwords = []



f = open("data/femalenames.txt", "r")
for x in f:
  female.append(x.strip().lower().capitalize() )

f = open("data/malenames.txt", "r")
for x in f:
    male.append(x.strip().lower().capitalize())

f = open("data/surnames.txt", "r")
for x in f:
    surnames.append(x.strip().lower().capitalize())

f = open("data/passwords.txt", "r")
for x in f:
    passwords.append(x.strip())


f = open("hackedusers.txt", "w")
f2 = open("users.txt", "w")

user = random.randint(0,USER_COUNT-1)



for i in range(USER_COUNT):
    names = male
    if random.randint(0,10) % 2 == 0:
        names = female
    fname = names[random.randint(1,len(names))-1]
    lname = surnames[random.randint(1,len(surnames))-1]
    password = passwords[random.randint(1, len(passwords)) - 1]
    m = hashlib.new("md5")
    m.update(x.encode("utf8"))
    hashedpassword = m.hexdigest()
    uname = (fname+"."+lname+"@pychain.io").lower()
    f.write(fname+":"+lname+":"+(uname+":").lower()+hashedpassword+"\n")
    if i==user:
        f2.write(uname+":"+password)


f.close()
f2.close()