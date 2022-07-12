# Racunarstvo u oblaku 
Domaci zadaci. 

## Domaci 1 - Docker
```
docker-compose up
```

## Domaci 2 - CWL
```
cwl-runner scatter-ann.cwl config.yaml
```

## Domaci 3 - Kubernetes
APP : http://k8s-master.unic.kg.ac.rs:30006/swagger/

Obucavanje modela za binarnu klasifikaciju

**/trainMlModel primer ulaza:**<br />
file: heart.csv fajl<br />
y_col: HeartDisease<br />
model_name: Heart model<br />
epochs: 30

**/predict primer ulaza:**<br />
file: heart_test.csv (fajl bez izlazne kolone)<br />
model_guid: 1353d934-01b9-11ed-8e3a-d2239dfcd098<br />


## Domaci 4 - Zookeeper
1. U folderu gde se nalazi apache-zookeeper izvrsiti komande:<br/>
```
sudo bin/zkServer.sh start
bin/zkCli.sh
```
3. Pokreniti skriptu pythonApp/start.sh<br />
4. Pokrenuti python app<br />
```
python3 app.py
```
(http://127.0.0.1:5000/swagger)

4. Pokrenuti aplikaciju na tri porta<br />

(http://127.0.1.1:8081/swagger-ui.html)
```
java -Dserver.port=8081 -Dzk.url=localhost:2181 -Dleader.algo=2 -jar target/bkatwal-zookeeper-demo-1.0-SNAPSHOT.jar
java -Dserver.port=8082 -Dzk.url=localhost:2181 -Dleader.algo=2 -jar target/bkatwal-zookeeper-demo-1.0-SNAPSHOT.jar
java -Dserver.port=8083 -Dzk.url=localhost:2181 -Dleader.algo=2 -jar target/bkatwal-zookeeper-demo-1.0-SNAPSHOT.jar
```
Obucavanje modela za binarnu klasifikaciju.

** /updateModel primer ulaza:**<br />
file: novi .h5 fajl koji ce zameniti stari. Primer f879783a-fc5e-11ec-be37-00155dd19498.h5
id: 1 - id kod odabrane instance

**/predict primer ulaza:**<br />
file: heart_test.csv (fajl bez izlazne kolone)<br />
id: 0 (paziti da se odabere model kome odgovaraju podaci za predikciju. Izvrsiti get /models i po naslovu videti o kom modelu se radi)<br />


## Domaci 5 - AWS 
Upaliti EC2 i pokrenuti app/app.py 
```
python3 app.py
```
Obucavanje modela za Boston Housing

Bucket - aleksandra-1025-2021<br/>
API Gateway - aleksandra_1025_2021<br/>

Primer poziva (POST metod): https://wnxt27xv1m.execute-api.eu-central-1.amazonaws.com/v1/predict?model_name=fragment1&dataset_name=predict (paziti da se fragment1.h5 i predict.csv nalaze u s3 skladistu)

Primer eventa:<br/> 
(INSERT) ubaciti fragment2.csv u s3 skladiste. Za proveravanje baze izvrsiti select * from aleksandra_1025_2021<br/> 
(UPDATE) ubaciti fragment2.csv u s3 skladiste za ponovno obucavanje modela. Za proveravanje baze izvrsiti select * from aleksandra_1025_2021<br/> 
(DELETE) obrisati fragment2.csv iz s3 skladista. Za proveravanje baze izvrsiti select * from aleksandra_1025_2021<br/> 



