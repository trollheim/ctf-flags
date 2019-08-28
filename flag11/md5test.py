import hashlib
import time


start = time.time()
print("hello")
end = time.time()
print(end - start)


start = time.time()
f = open("data/passwords.txt", "r")
i = 0;
for x in f:
    m = hashlib.new("md5")
    m.update(x.encode("utf8"))
    print(m.hexdigest())
    i=i+1
    if i % 1000 == 0:
        print(str(i)+"elements in "+str(time.time()-start))


