import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.initializers import HeNormal

# Set random seed for reproducibility
np.random.seed(0)
tf.random.set_seed(0)

# Create a deep neural network with sigmoid activation functions
model = Sequential()
model.add(Dense(128, input_dim=1, activation='sigmoid'))
for _ in range(10):
    model.add(Dense(128, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='sgd', loss='mean_squared_error')

# Generate simple data
x = np.linspace(-1, 1, 200)
y = x ** 2

# Train the model and observe the vanishing gradients
history = model.fit(x, y, epochs=100, verbose=0)

# Get the weights of the first layer
weights = model.layers[0].get_weights()[0]

# Plot the weights of the first layer
plt.plot(weights)
plt.title('Weights of the first layer')
plt.show()

# Mitigate the vanishing gradient problem using ReLU and He Initialization
model = Sequential()
model.add(Dense(128, input_dim=1, activation='relu', kernel_initializer=HeNormal()))
for _ in range(10):
    model.add(Dense(128, activation='relu', kernel_initializer=HeNormal()))
model.add(Dense(1, activation='relu', kernel_initializer=HeNormal()))

model.compile(optimizer='adam', loss='mean_squared_error')

# Train the modified model
history = model.fit(x, y, epochs=100, verbose=0)

# Get the weights of the first layer after mitigation
weights = model.layers[0].get_weights()[0]

# Plot the weights of the first layer after mitigation
plt.plot(weights)
plt.title('Weights of the first layer with ReLU and He Initialization')
plt.show()
