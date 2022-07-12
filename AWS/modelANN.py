import os
import uuid
import warnings
import boto3
import numpy as np
import pandas as pd
from tensorflow import keras
from keras import Sequential
from keras.models import load_model
from sklearn.model_selection import train_test_split
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler

UPLOAD_FOLDER = 'models'
s3 = boto3.client("s3")
dynamo = boto3.client("dynamodb")

table_name = "aleksandra_1025_2021"
s3_bucket_name = "aleksandra-1025-2021"


class ANN:


    def train_model(self, file_name, epochs, batch_size):

        try:

            s3.download_file(Bucket = s3_bucket_name, Key = file_name+".csv", Filename = os.path.join(UPLOAD_FOLDER, file_name+".csv"))

            y_col = "MEDV"
            column_names = ['CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS','RAD','TAX','PTRATIO','B','LSTAT','MEDV']
            df = pd.read_csv(os.path.join(UPLOAD_FOLDER, file_name+".csv"),header=None,names=column_names)

            # Split data
            X = df.drop([y_col], axis = 1)
            y = df[y_col].values
            X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)

            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train) 
            X_test=scaler.transform(X_test) 
            input_layer = len(df.columns)-1
            classifier = Sequential()
            classifier.add(Dense(input_layer,activation='relu',input_shape=(input_layer,), kernel_regularizer=keras.regularizers.l2(0.2)))
            classifier.add(Dense(units = 28, activation = 'relu', kernel_regularizer=keras.regularizers.l2(0.2)))
            classifier.add(Dense(units = 13, activation = 'relu', kernel_regularizer=keras.regularizers.l2(0.2)))
            classifier.add(Dense(units = 1))
            classifier.compile(optimizer = 'adam', loss = 'mse', metrics = ['mae'])
            classifier.fit(X_train, y_train, batch_size = batch_size, epochs = epochs, verbose=0)
            scores = classifier.evaluate(X_train, y_train, verbose=0)

            # Save model locally
            classifier.save(os.path.join(UPLOAD_FOLDER, file_name + ".h5"))

            s3.upload_file(Filename = os.path.join(UPLOAD_FOLDER, file_name + ".h5"), Bucket = s3_bucket_name, Key = file_name +".h5")

            #Predict on test.csv
            df = pd.read_csv(os.path.join(UPLOAD_FOLDER,"test.csv"),header=None,names=column_names)
            X = df.drop([y_col], axis = 1)
            y = df[y_col].values
            scores = classifier.evaluate(X_train, y_train, verbose=0)

            #Insert into database
            self.delete_from_database(os.path.splitext(file_name)[0])
            dynamo.put_item(
                TableName = table_name,
                Item = {
                    'file_name': {'S': os.path.splitext(file_name)[0]+".csv"},
                    'mse': {'S': str(round(scores[0],2))},
                    'mae': {'S': str(round(scores[1],2))}
                }
            )           
            return "OK"
        except Exception as e:
            print(e)
            return "non"


    def predict_value(self, model_name, dataset_name):
        try:
            #save from s3
            s3.download_file(Bucket = s3_bucket_name, Key = model_name+".h5", Filename = os.path.join(UPLOAD_FOLDER, model_name+".h5"))
            s3.download_file(Bucket = s3_bucket_name, Key = dataset_name+".csv", Filename = os.path.join(UPLOAD_FOLDER, dataset_name+".csv"))
        except Exception as e:
            print("Folder does not exists.")
            return 500
       
        model = load_model(os.path.join(UPLOAD_FOLDER, model_name + ".h5"))
        X_test = pd.read_csv(os.path.join(UPLOAD_FOLDER, dataset_name+".csv"))
        config = model.get_config() 
        numInputs = config["layers"][0]["config"]["batch_input_shape"][1]
        if (X_test.shape[1] != numInputs):
            return numInputs

        return model.predict(X_test)

    def delete(self, model_name):
        try:
           s3.delete_object(Bucket = s3_bucket_name, Key = model_name+".h5")
        except Exception as e:
            print("Folder does not exists.")
         
        self.delete_from_database(model_name)

    def delete_from_database(self, model_name):
        try:
            table = boto3.resource("dynamodb").Table(table_name)
            table.delete_item(
                Key = {'file_name': model_name+".csv"})
        except Exception as e:
            print("No model in database")
