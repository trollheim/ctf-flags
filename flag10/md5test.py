import hashlib
import time


start = time.time()
print("hello")
end = time.time()
print(end - start)

xx ='ce601bb436d05cd27f070d5449375579'

start = time.time()
f = open("data/passwords.txt", "r")
i = 0;
for x in f:
    x ='180552'
    m = hashlib.new("md5")
    m.update(x.encode("utf8"))
    p = m.hexdigest()
    if p == xx:

        print(xx)
    i=i+1
    # if i % 1000 == 0:
    #     print(str(i)+"elements in "+str(time.time()-start))


