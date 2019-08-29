FROM flag-base
ARG flagval=flag12


# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY start.sh /app


COPY static /app/static


RUN echo "$flagval" >> /app/flag.txt

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "start.sh"]