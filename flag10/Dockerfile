FROM flag-base
ARG flag=flag10


# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY start.sh /app
COPY usergen.py /app

COPY static /app/static
COPY data /app/data

# RUN python3 usergen.py
# does not work for some reason, need to be investigated
# workaround
COPY hackedusers.txt /app
COPY users.txt /app

RUN echo "$flag" >> /app/flag.txt

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "start.sh"]