# -*- coding: utf-8 -*-
"""Copy_of_Crop_Recommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JU_S7aDBYzdCkyYbOmlDgeQplkUY7dt9

Importing the Packages
"""

import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow import keras

train_accuracy = {}
test_accuracy = {}

df = pd.read_csv('/content/Crop_recommendation.csv')

df.iloc[:,:]

"""Printing the summary of the data using info() method."""

df.info()

"""Printing the first ten rows from the dataset using head() method."""

df.head(10)

"""Finding whether there are any null values in the dataset"""

df.isnull().sum()

"""##Exploratory Data Analysis"""

plt.figure(figsize=(10,9))
df.boxplot()
plt.show()

df.corr()

columns = df.columns[:-1]
plt.figure(figsize=(16,13))

i=1
for col in columns[:-1]:
  plt.subplot(3,3,i)
  sns.histplot(df[col], bins=30)
  i+=1
plt.show()

sns.histplot(df[columns[-1]],bins=30)

plt.figure(figsize=(13,12))
sns.histplot(df[columns])

for col in columns:
  plt.figure(figsize=(28,4))
  sns.barplot(x="label",y=col, data=df)
  plt.title(f"{col} vs Crop Type")
  plt.show()

sns.pairplot(df)

sns.pairplot(df,hue='label')

plt.figure(figsize=(12,10))
sns.heatmap(df.corr(), annot=True, center=0)
plt.show()

plt.figure(figsize=(20,15))
sns.scatterplot(data=df)

x = df['label'].value_counts().to_dict()

x_v = list(x.values())
x_k = list(x.keys())
plt.pie(x_v, labels=x_k, shadow=True)
plt.show()

"""Handling Categorical Data

Creating the list of output labels
"""

labels = df['label'].unique()

"""Creating the dictionary of categorical values and their labels"""

labeled_data = {}
j=0
for i in labels:
  labeled_data[i] = j
  j+=1

print(labeled_data)

label_values = list(labeled_data.values())

print(labels)
print("\n\n")
print(label_values)

labels

"""Label encoding the categorical values and adding the label_encoded column in the dataframe with encoded values"""

df['label_encoded'] = df.label.map(labeled_data)

df.head()

df.describe()

"""Separting the Input and output features in the dataset"""

X = df.drop(['label','label_encoded'],axis=1)
X.head()

y = df['label_encoded']
y.head()

"""Splitting the data into train set and test set"""

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2, random_state=1)

"""Feature Scaling: Scaling the numerical data"""

sc = StandardScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

sc.mean_

np.sqrt(sc.var_)

X_train.shape

"""# ANN Model

Building the architecture of the ANN Model
"""

model = tf.keras.Sequential()
model.add(keras.layers.Dense(28,input_shape=(7,),activation='relu'))
model.add(keras.layers.Dense(64,input_shape=(7,), activation='relu'))
model.add(keras.layers.Dense(28,input_shape=(7,), activation='relu'))
model.add(keras.layers.Dense(22,input_shape=(7,), activation='softmax'))

model.compile(
    optimizer = 'adam',
    loss = 'sparse_categorical_crossentropy',
    metrics = ['accuracy']
)

"""Architecture of the Neural Network"""

model.summary()

"""Fitting the training data to the neural network model"""

history = model.fit(x=X_train, y = y_train,epochs=300,batch_size=50 )

"""Plotting the Loss and accuracy of the training data"""

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""Evaluating the model on test data"""

eval = model.evaluate(X_test,y_test)

train_accuracy['ANN model'] = history.history['accuracy'][-1]*100
test_accuracy['ANN model'] = eval[-1]*100

"""Testing the model"""

from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/MyDrive/output.jpg'

test1 = sc.transform(np.array([[30,28,30,32,52,5,98]]))
pre1 = np.argmax(model.predict(test1))
print(labels[pre1])
img_path = str(labels[pre1])+'.jpg'
x = plt.imread(file_path+img_path)
plt.imshow(x)
plt.show()

test2 = sc.transform(np.array([[104, 18, 30, 24, 60, 7, 141]]))
pre2 = np.argmax(model.predict(test2))
print(labels[pre2])
img_path = str(labels[pre2])+'.jpg'
x = plt.imread(file_path+img_path)
plt.imshow(x)
plt.show()

model.save("Crop_Recommendation.h5")