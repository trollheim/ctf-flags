FROM flag-base
ARG flagval=flag10


# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY start.sh /app
COPY usergen.py /app

COPY static /app/static
COPY data /app/data

RUN usergen.sh
RUN echo "$flag" >> /app/flag.txt

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "start.sh"]