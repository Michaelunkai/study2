import tensorflow as tf

# Create a simple neural network with ReLU activation
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Print the model summary
model.summary()

