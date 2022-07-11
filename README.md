# Racunarstvo u oblaku 
Domaci zadaci

## Domaci 1 - docker
```
docker-compose up
```

## Domaci 2 - CWL
```
cwl-runner scatter-ann.cwl config.yaml
```

## Domaci 3 - Kubernetes
APP : http://k8s-master.unic.kg.ac.rs:30006/swagger/

## Domaci 4 - Zookeeper
1. Pokreniti skriptu pythonApp/start.sh

2. Pokrenuti python app
```
python app.py
```
   (http://127.0.0.1:5000/swagger)

3. Pokrenuti aplikaciju na tri porta

   (http://127.0.1.1:8081/swagger-ui.html)
```
java -Dserver.port=8081 -Dzk.url=localhost:2181 -Dleader.algo=2 -jar target/bkatwal-zookeeper-demo-1.0-SNAPSHOT.jar
java -Dserver.port=8082 -Dzk.url=localhost:2181 -Dleader.algo=2 -jar target/bkatwal-zookeeper-demo-1.0-SNAPSHOT.jar
java -Dserver.port=8081 -Dzk.url=localhost:2181 -Dleader.algo=2 -jar target/bkatwal-zookeeper-demo-1.0-SNAPSHOT.jar
```

## Domaci 5 - AWS 
Upaliti EC2 i pokrenuti app/app.py

Bucket - aleksandra-1025-2021
API Gateway - aleksandra_1025_2021
Primer poziva: https://wnxt27xv1m.execute-api.eu-central-1.amazonaws.com/v1/predict?model_name=fragment1&dataset_name=predict



