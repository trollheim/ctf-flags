FROM flag-base
ARG flagval=flag8



RUN apt-get update && apt-get install -y mongodb
# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY start.sh /app
COPY inseruser.js /app

COPY static /app/static

RUN pip3 install pymongo

RUN echo "$flagval" >> /app/flag.txt

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "start.sh"]