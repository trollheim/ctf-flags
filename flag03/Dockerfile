FROM madtroll/myctf-base


ARG flag=flag3


# Set the working directory to /app

# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY start.sh /app

COPY static /app/static
COPY node /app/node
COPY users.txt  /app

RUN echo "$flag" >> /app/flag.txt
# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
CMD ["sh", "start.sh"]