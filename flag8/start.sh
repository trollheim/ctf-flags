mongod --dbpath . &
sleep 5
mongo  127.0.0.1/flagdb inseruser.js
python3.6 webapp.py
