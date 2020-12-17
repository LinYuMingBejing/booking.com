># Booking.com
### Enviroment:
* Ubuntu: 16.04 
* Python: 3.6.2
* Backend: Flask
* Test: Swagger
* Database: MongoDB, Redis
* Asynchronous: Celery (Redis)
* Monitoring Tool: Supervisor, Prometheus, Grafana
* Collecting Logs: Logstash


#### Install Docker
```
$ sudo apt-get update

$ sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

$ sudo apt-key fingerprint 0EBFCD88

$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu
$(lsb_release -cs)
stable"

$ sudo apt-get update

$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### Install Docker Compose
```
$ sudo apt install docker-compose
```

### Deploy Booking.com Application
* Deploy
```
$ cd ./docker_stg
$ sudo docker-compose up --build -d
```

* Check docker process
```
$ sudo docker ps
```

* Get docker log
```
$ sudo docker-compose logs --tail=20 -f flask
```

#### Swagger 
* http://localhost/

![swagger](https://img.onl/pluv8Q)


#### Monitor process
```
$ supervisorctl
```

![supervisorctl](https://github.com/LinYuMingBejing/booking.com/blob/master/imgs/supervosor.png)


* http://localhost:9001

![supervisor_web](https://img.onl/wmlqSJ)


#### Monitor uwsgi application
```
uwsgitop 127.0.0.1:5002
```

![uwsgitop](https://github.com/LinYuMingBejing/booking.com/blob/master/imgs/uwsgitop.png)


#### Monitor celery worker 
* http://localhost:5001/tasks

![flower](https://img.onl/S5P6iC)


#### Prometheus Monitor
* http://localhost:9090/targets

![Prometheus](https://img.onl/6vdblM)


#### Grafana Monitor
* http://localhost:3000
* Username: admin
* Password: pass

![Grafana](https://img.onl/7RoMbq)


#### Nginx Log Monitor
* http://localhost:5601
![logstash](https://img.onl/MXXRSG)


#### Note1: How to allow certain ips connect mongodb?

* vim /etc/mongod.conf
```
    # bindIp: 127.0.0.1
    bindIp: 0.0.0.0  
```

* restart mongodb
```
$ sudo service mongod restart
$ sudo service mongod status
```

* firewall settings
```
$ sudo ufw enable
$ sudo ufw deny  from 192.168.18.0/24 to any port 27017
$ sudo ufw allow from 192.168.18.0/24 to any port 27017
$ sudo ufw status
```

#### Note2: How to create multiple user on mongodb?

* create user
```
> use booking;
switched to db booking
> db.createUser(
  {
    user: "dbadmin",
    pwd: "StrongPassword",
    roles: [ { role: "readWrite", db: "booking" } ]
  }
)
> exit
bye
```

* vim /etc/mongod.conf 
```
security:
  authorization: enabled
```

* restart mongodb
```
$ sudo service mongod restart
$ sudo service mongod status
```

> ##### Reference
> * https://blog.techbridge.cc/2019/08/26/how-to-use-prometheus-grafana-in-flask-app/