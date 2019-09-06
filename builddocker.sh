docker build -t madtroll/myctf-base .

# find . -depth 1 -type d |grep flag|cut -c3- |xargs -I {}



rm ./core/flags.txt
find . -depth 1 -type d |cut -c3- |grep flag | while read dir;do flag=`python3 flaggen.py`; echo "$dir:$flag">>./core/flags.txt; docker build -t "$dir" "$dir" --build-arg flag="$flag"; done
