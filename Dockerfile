FROM ubuntu:16.04


run apt-get update
run apt-get install -y software-properties-common
run apt-get install -y curl
RUN add-apt-repository ppa:jonathonf/python-3.6
run curl -sL https://deb.nodesource.com/setup_10.x |  bash -
run apt-get update

run apt-get install -y nodejs


RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv


# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

# Install any needed packages specified in requirements.txt
run apt-get install -y libpangocairo-1.0-0 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libnss3 libcups2 libxss1 libxrandr2 libgconf2-4 libasound2 libatk1.0-0 libgtk-3-0
WORKDIR /app
COPY requirements.txt /app

run npm i puppeteer
RUN python --version
RUN pip install cherryPy
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
#RUN pip install --trusted-host pypi.python.org -r requirements.txt