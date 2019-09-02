import os

# f = []
# for (dirpath, dirnames, filenames) in os.walk("./flag17/git"):
#     print(dirnames)
#     f.extend(filenames)
#
#     break
# print(f)


def traversal(dir):
    for (dirpath, dirnames, filenames) in os.walk(dir):
        f = open(dirpath+"/index.html", "w+")
        f.write("<html><body>"+
                "<h1>Index of "+
                dirpath.replace("./flag17/git", "/.git")
                +"<table><tr><th>Name</th></tr>\n")
        for d in dirnames:
            f.write("<tr><td><a href='"+dirpath.replace("./flag17/git", "/.git")+"/"+d+"'>"+d+"</a></td></tr>\n")
        for d in filenames:
            f.write("<tr><td><a href='" + dirpath.replace("./flag17/git", "/.git") + "/"+d+"'>" + d + "</a></td></tr>\n")
        f.write("</table></body></html>")
        f.close()




def remove(dir):
    for (dirpath, dirnames, filenames) in os.walk(dir):
        os.remove(dirpath+"/index.html")

# remove("./flag17/git")
# traversal("./flag17/git")

for (dirpath, dirnames, filenames) in os.walk("./flag17/git"):
    for d in dirnames:
        print("'"+dirpath.replace("./flag17/git","/.git") + "/" + d+"/',")
