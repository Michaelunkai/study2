import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense

# Generate dummy dataset
data = np.random.rand(1000, 10, 1)
labels = np.random.randint(2, size=(1000, 1))

# Define the RNN model
model = Sequential()
model.add(SimpleRNN(50, activation='relu', input_shape=(10, 1)))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(data, labels, epochs=10, batch_size=32)

# Evaluate the model
loss, accuracy = model.evaluate(data, labels)
print(f'Loss: {loss}, Accuracy: {accuracy}')
