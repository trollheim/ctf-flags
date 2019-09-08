FROM madtroll/myctf-base

# install SQLite
RUN apt-get install sqlite3 libsqlite3-dev

# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY start.sh /app
COPY database.db /app

COPY static /app/static


EXPOSE 8080

ENTRYPOINT ["/bin/sh", "start.sh"]