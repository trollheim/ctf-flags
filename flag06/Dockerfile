FROM madtroll/myctf-base


ARG flag=flag6


# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY start.sh /app

COPY static /app/static
COPY database.db /app
RUN sqlite3 database.db "insert into tblflag( 'flag' ) values ( '${flag}' )"

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "start.sh"]