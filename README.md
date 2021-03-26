# Airflow example


### Run Airflow locally 

Get composer config : 
```
docker-compose -f airflow-stack/airflow-docker-compose.yml config
```

**Required** permissions to RUN : 
```
sudo chmod -R 777 airflow-stack/dags/ airflow-stack/logs/ airflow-stack/postgres-data/
```

Build and run cluster
```
docker-compose -f airflow-stack/airflow-docker-compose.yml up -d --build
```

Airflow UI [localhost:8282](http://localhost:8282)

- list users
```
docker exec airflow-stack_webserver_1 /bin/sh -c "airflow users list"
```

- create admin user (admin/test) to login
```
docker exec airflow-stack_webserver_1 /bin/sh -c "airflow users create -r Admin -u admin -e admin@example.com -f admin -l user -p test"
```

#### restart local cluster
```
docker start $(docker ps -a | grep 'airflow-stack_*' | awk '{print $1}')
docker stop $(docker ps -a | grep 'airflow-stack_*' | awk '{print $1}')

####
docker rm -f $(docker ps -a | grep 'airflow-stack_*' | awk '{print $1}')

sudo ./airflow-stack/purge-volumes-data.sh
```

#### utils
```
cp -r active_dags/. airflow-stack/dags/
  
## Or :

docker cp active_dags/. airflow-stack_scheduler_1:/opt/airflow/dags/.

docker exec -it airflow-stack_scheduler_1 /bin/bash
```