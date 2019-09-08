PORT=27000


docker run -dti -p0.0.0.0:"$PORT":8080 core

let flagport=PORT;
find . -depth 1 -type d|sort|cut -c3- |grep flag | while read dir; \
               do \
                let flagport=flagport+1; \
                echo "running flag $dir "
                docker run -dti -p0.0.0.0:"$flagport":8080 "$dir" ; \
               done;
