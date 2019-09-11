rm ./core/flags.txt
find . -depth 1 -type d |cut -c3- |grep flag |sort | while read dir; \
               do \
                flag=`python3 flaggen.py`;\
                echo "$dir:$flag">>./core/flags.txt;\
                docker build -t "$dir" "$dir" --build-arg flag="$flag"; --no-cache\
                cp users.txt "$dir"; \

               done
 cp users.txt ./core
(cd core ; python3 ./dbutil.py)
 docker build -t core ./core

