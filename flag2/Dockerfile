FROM flag-base

ARG flag=flag2

#FROM python:3.7-slim

# Set the working directory to /app

# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY start.sh /app

COPY static /app/static
COPY node /app/node
RUN echo "$flag" >> /app/flag.txt

EXPOSE 8080

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
CMD ["sh", "start.sh"]