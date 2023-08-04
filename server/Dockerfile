FROM python:3.11.4

RUN apt-get -y update
RUN apt-get -y install python3-pip python3-dev libpq-dev

RUN pip install --upgrade pip

WORKDIR /usr/srv/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8000
