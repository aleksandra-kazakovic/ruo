import os
from statistics import mode
import uuid
import warnings
import numpy as np
import pandas as pd
from tensorflow import keras
from modelDatabase import Database
from keras import Sequential
from keras.models import load_model
from sklearn.model_selection import train_test_split
from keras.layers import Dense

UPLOAD_FOLDER = 'models'

class ANN:
    
    def train_model(self, file_path, y_col, epochs, batch_size):   
        #Split data
        try:
            df = pd.read_csv(os.path.join(file_path))
            cat_columns = df.select_dtypes(['object']).columns
            df[cat_columns] = df[cat_columns].apply(lambda x: pd.factorize(x)[0])
            X = df.drop([y_col], axis = 1)
            y = df[y_col].values
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

            X_test.to_csv('heart_test.csv', index=False)

            
            #Train model
            input_layer = len(df.columns)-1
            print("INPUTTT "+ str(input_layer))
            classifier = Sequential()
            classifier.add(Dense(units=input_layer, activation = 'relu', input_dim = input_layer))
            classifier.add(Dense(units = 3, activation = 'relu'))
            classifier.add(Dense(units = 1, activation = 'sigmoid'))
            classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy', 'AUC'])
            classifier.fit(X_train, y_train, batch_size = batch_size, epochs = epochs, verbose=0)

            #Evaluation
            scores = classifier.evaluate(X_test, y_test, verbose=0)

            # Save model
            #params = yaml.safe_load(open('params.yaml'))
            guid = uuid.uuid1()
            guid = str(guid)
            classifier.save(os.path.join(UPLOAD_FOLDER, guid + ".h5"))

            return guid, scores[0], scores[1]
        except Exception as e:
            print(e)
            return 'non', 0, 0


    def predict_value(self, file_name, dataset_path):
        try:
            model = load_model(os.path.join(UPLOAD_FOLDER, file_name + ".h5"))
            X_test = pd.read_csv(os.path.join(dataset_path))
            config = model.get_config() 
            numInputs = config["layers"][0]["config"]["batch_input_shape"][1]
            if (X_test.shape[1] != numInputs):
                return numInputs

            return model.predict(X_test)
        except Exception as e:
            print(e)
            return 500