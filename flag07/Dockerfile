FROM madtroll/myctf-base


ARG flag=flag7




# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY start.sh /app
COPY inseruser.js /app

COPY static /app/static


RUN echo "$flag" >> /app/flag.txt

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "start.sh"]