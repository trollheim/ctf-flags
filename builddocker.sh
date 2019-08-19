docker build -t flag-base .
ls -ld */  |grep flag| awk '{print $9}' |xargs -I {} docker build -t '{}'latest '{}'