import os
from flask_mysqldb import MySQL
from modelMl import ModelMl

class Database():

    def __init__(self, app):

        app.config['MYSQL_HOST'] = '127.0.0.1'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'kazak'
        app.config['MYSQL_DB'] = 'appZookeeper'
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

    def get_model_by_id(self, id):
        cur = self.mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM models WHERE id = " +str(id))
        if resultValue > 0:
            datas = cur.fetchall()
            for data in datas:
                return ModelMl(data[0], data[1], data[2], data[3], data[4], data[5])

    def delete_model_by_id(self, id):
        cur = self.mysql.connection.cursor()
        resultValue = cur.execute("DELETE FROM models WHERE id = " +str(id))
        self.mysql.connection.commit()
        cur.close()
        

    


       
