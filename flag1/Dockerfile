FROM python:3.7-slim
from node:8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY webapp.py /app
COPY requirements.txt /app
COPY static /app/static
copy node/flag1-user.js /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
run npm install puppeteer
# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
#ENV NAME World
run python webapp.py
# Run app.py when the container launches
CMD ["node", "flag1-user.js"]