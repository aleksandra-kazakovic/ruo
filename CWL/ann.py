import sys
import pandas as pd
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense
import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import warnings

file_path = sys.argv[1]
k = int(sys.argv[2])
current_fold = int(sys.argv[3])

df = pd.read_csv(file_path)

chunk_size = int(len(df) / k)

cat_columns = df.select_dtypes(['object']).columns
df[cat_columns] = df[cat_columns].apply(lambda x: pd.factorize(x)[0])

X = df.drop(['HeartDisease'], axis = 1)
y = df.HeartDisease.values

X_train = X.iloc[np.r_[0:current_fold*chunk_size, chunk_size*(current_fold+1):len(X)]]
y_train = y[np.r_[0:current_fold*chunk_size, chunk_size*(current_fold+1):len(X)]]
X_test = X[chunk_size*current_fold:chunk_size*(current_fold+1)]
y_test = y[chunk_size*current_fold:chunk_size*(current_fold+1)]

classifier = Sequential()
classifier.add(Dense(units=11, activation = 'relu', input_dim = 11))
classifier.add(Dense(units = 3, activation = 'relu'))
classifier.add(Dense(units = 1, activation = 'sigmoid'))

classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy', 'AUC'])

classifier.fit(X_train, y_train, batch_size = 10, epochs = 10, verbose=0)

scores = classifier.evaluate(X_test, y_test, verbose=0)
print("%.2f %.2f" % (scores[1]*100, scores[2]*100))