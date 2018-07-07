import os
#Warning:Your CPU supports instructions that this TensorFlow binary was not compiled
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import pandas as pd
import numpy as np
import time

from keras.datasets import mnist
from keras.models import Model #泛型模型
from keras.layers import Dense, Input
from keras import regularizers

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve,auc
import tf_input_data as input_data

print(time.strftime('%Y/%m/%d %T')+" - Start "+'-'*40 )

df = pd.read_csv("C:/Users/houz/OneDrive/DataSet/german_credit_data/german_credit_data.csv")

LABELS = ["Normal", "Fraud"]
count_classes = pd.value_counts(df['Creditability'], sort = True)

count_classes.plot(kind = 'bar', rot=0)
plt.title("Transaction class distribution")
plt.xticks(range(2), LABELS)
plt.xlabel("Class")
plt.ylabel("Frequency")

#plt.show()

print(df.columns)

#DataSet
RANDOM_SEED = 42
X_train, X_test = train_test_split(df, test_size=0.2, random_state=RANDOM_SEED)
X_train = X_train[X_train.Creditability == 0]
X_train = X_train.drop(['Creditability'], axis=1)

y_test = X_test['Creditability']
X_test = X_test.drop(['Creditability'], axis=1)

X_train = X_train.values
X_test = X_test.values

#Model
input_dim = X_train.shape[1]
encoding_dim = 22
input_layer = Input(shape=(input_dim, ))
encoder = Dense(encoding_dim, activation="tanh",activity_regularizer=regularizers.l1(10e-5))(input_layer)
encoder = Dense(int(encoding_dim / 2), activation="relu")(encoder)
decoder = Dense(int(encoding_dim / 2), activation='tanh')(encoder)
decoder = Dense(input_dim, activation='relu')(decoder)
autoencoder = Model(inputs=input_layer, outputs=decoder)

#Train
nb_epoch = 100
batch_size = 32

autoencoder.compile(optimizer='adam',
                    loss='mean_squared_error',
                    metrics=['accuracy'])

history = autoencoder.fit(X_train, X_train,
                          epochs=nb_epoch,
                          batch_size=batch_size,
                          shuffle=True,
                          validation_data=(X_test, X_test),
                          verbose=1).history

#Performance
predictions = autoencoder.predict(X_test)
mse = np.mean(np.power(X_test - predictions, 2), axis=1)
error_df = pd.DataFrame({'reconstruction_error': mse,
                         'true_class': y_test})

fpr, tpr, thresholds = roc_curve(error_df.true_class, error_df.reconstruction_error)
roc_auc = auc(fpr, tpr)

plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, label='AUC = %0.4f'% roc_auc)
plt.legend(loc='lower right')
plt.plot([0,1],[0,1],'r--')
plt.xlim([-0.001, 1])
plt.ylim([0, 1.001])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()


plt.plot(history['loss'])
plt.plot(history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right');
plt.show()

print(time.strftime('%Y/%m/%d %T')+" - End "+'-'*42 )
