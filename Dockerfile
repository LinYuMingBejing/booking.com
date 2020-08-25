FROM            python:3.6-onbuild
MAINTAINER      a828215362@gmail.com

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools 

RUN mkdir -p /usr/src/api  /etc/prometheus  /etc/supervisor/conf.d /var/log/supervisord

WORKDIR /usr/src/api

COPY requirements.txt /usr/src/api/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/api
COPY entrypoint.sh /
COPY supervisord.conf /etc/
COPY supervisor-uwsgi.conf  supervisor-worker.conf /etc/supervisor/conf.d/  

RUN  chmod +x /entrypoint.sh 