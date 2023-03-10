# -*- coding: utf-8 -*-
"""Logistic Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jCrr7EisIZW4XOtMvXJevv5t324aXq8r
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""# Read and Shuffle"""

df = pd.read_csv("customer_data.csv")
df.head()

np.random.shuffle(df.values)
df.head()

plt.figure(figsize=(3,3))
sns.heatmap(df.corr(),annot=True)
plt.show()

X = df[df.columns[:-1]]
Y = df['purchased']
Y.head()

"""# Normalize"""

x_min = X.min(axis=0)
x_max = X.max(axis=0)

normalized_X = (X - x_min) / (x_max - x_min)
normalized_X.head()

"""# Splitting"""

col = normalized_X.shape[0]
x_train = normalized_X[:int(col*0.8)]
x_test = normalized_X[int(col*0.8):]
y_train = Y[:int(col*0.8)]
y_test = Y[int(col*0.8):]

"""# Model"""

class LogisticRegression:
  def __init__(self, learning_rate):
    self.learning_rate = learning_rate

  def _sigmoid(self, x):
    return 1 / (1 + np.exp(-np.dot(x, (self.theta).T) - self.b))
    
  def _cost_function(self):
    z = self._sigmoid(self.X)
    loss = self.Y * np.log10(z) + (1-self.Y) * np.log10(1-z)
    m = (self.X).shape[0]
    cost = np.sum(loss) / m
    return cost

  def _gradient_descent(self):
    m = (self.X).shape[0]
    for i in range(0,1000):
      z = (self._sigmoid(self.X))
      temp = self.Y - z
      temp2 = np.dot(temp.T, self.X)
      dw = temp2 / m
      db = np.sum(temp) / m
      self.theta += self.learning_rate * dw
      self.b += self.learning_rate * db

  def fit(self, X, Y):
    self.X = X
    self.Y = (np.array(Y)).reshape(Y.shape[0],1)
    self.theta = np.zeros((1, X.shape[1]))
    self.b = 0
    self._gradient_descent()

  def predict(self, x):
    results = (self._sigmoid(x))
    return (results >= 0.5).astype(int)

model = LogisticRegression(0.01)
model.fit(x_train, y_train)

results = model.predict(x_test)

y_test = (np.array(y_test)).reshape(y_test.shape[0],1)
def accuracy(results, y_test):
  acc = (results == y_test).astype(int)
  return (acc.sum()/acc.shape[0])

"""# Try different learning rate"""

rates = np.zeros((40,))
accuracies = np.zeros((40,))

rate = 0.001
for i in range(40):
  model = LogisticRegression(rate)
  model.fit(x_train, y_train)
  results = model.predict(x_test)
  rates[i] = rate
  accuracies[i] = accuracy(results, y_test)
  rate += 0.02

plt.scatter(rates, accuracies)
plt.title('Accuracy of different learning rates')
plt.xlabel('Learning Rate')
plt.ylabel('Accuracy')
plt.show()

