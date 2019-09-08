FROM madtroll/myctf-base


ARG flag=flag5

# install SQLite
RUN apt-get install sqlite3 libsqlite3-dev

# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY start.sh /app

COPY static /app/static
COPY database.db /app
RUN sqlite3 database.db "insert into tblflag( 'flag' ) values ( '${flag}' )"

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "start.sh"]