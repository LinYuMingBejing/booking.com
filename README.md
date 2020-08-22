># Booking.com
### Enviroment:
* Ubuntu: 16.04 
* Python: 3.6.2
* Backend: Flask
* Database: MongoDB, Redis
* Asynchronous: Celery (Redis)
* Monitoring Tool: Supervisor

### Install Docker
* sudo apt-get update

* sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

* curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

* sudo apt-key fingerprint 0EBFCD88

* sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu
$(lsb_release -cs)
stable"

* sudo apt-get update

* sudo apt-get install docker-ce docker-ce-cli containerd.io


### Install Docker Compose
* sudo apt install docker-compose



### Deploy Application
* Deploy
```
cd ./docker_stg
sudo docker-compose up --build -d
```

* Check docker process
```
sudo docker ps
```

* Get docker log
```
sudo docker-compose logs --tail=20 -f flask
```

### Monitor process
```
supervisorctl
```
![supervisorctl](https://img.onl/UQlnTg)

### Monitor uwsgi application
```
uwsgitop 127.0.0.1:5002
```
![uwsgitop](https://img.onl/YApRig)

### Monitor celery worker 
```
http://localhost:5001/dashboard
```
![flower](https://img.onl/QiHaVX)