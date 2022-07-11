import os
from flask_mysqldb import MySQL
from modelMl import ModelMl

class Database():

    def __init__(self, app):


        app.config['MYSQL_HOST'] = os.environ['HOST']
        app.config['MYSQL_PORT'] = int(os.environ['PORT'])
        app.config['MYSQL_USER'] = os.environ['USER']
        app.config['MYSQL_PASSWORD'] = os.environ['PASSWORD']
        app.config['MYSQL_DB'] = os.environ['DB_NAME']

        
        # app.config['MYSQL_HOST'] = 'localhost'
        # app.config['MYSQL_PORT'] = 3306
        # app.config['MYSQL_USER'] = 'root'
        # app.config['MYSQL_PASSWORD'] = ''
        # app.config['MYSQL_DB'] = 'appKubernetes'

        self.mysql = MySQL(app)
        
        

    def create_table(self):
        cur = self.mysql.connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS models ( `id` INT NOT NULL AUTO_INCREMENT, `model_name` VARCHAR(255) NOT NULL, `guid` VARCHAR(255) NOT NULL, `path` VARCHAR(255) NOT NULL, `accuracy` FLOAT NOT NULL, `auc` FLOAT NOT NULL, PRIMARY KEY (`id`))")
        self.mysql.connection.commit()
        cur.close()

    def insert_model(self, model_name, guid, path, accuracy, auc):
        self.create_table()
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO models(model_name, guid, path, accuracy, auc) values('" + model_name + "', '" + guid + "', '" + path +"', " + str(accuracy) + ", " + str(auc) + ")")
        self.mysql.connection.commit()
        cur.close()

    def get_models(self):
        self.create_table()
        cur = self.mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM models")
        if resultValue > 0:
            datas = cur.fetchall()
            models = []
            for data in datas:
                models.append(ModelMl(data[0], data[1], data[2], data[3], data[4], data[5]))
            return models
        return []


       
