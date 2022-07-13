

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

