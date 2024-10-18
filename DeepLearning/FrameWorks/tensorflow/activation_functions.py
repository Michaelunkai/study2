import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def plot_activation_function(func, x):
    y = func(x)
    plt.plot(x, y)
    plt.title(func.__name__)
    plt.xlabel('Input')
    plt.ylabel(' ')
    plt.grid()
    plt.show()

def main():
    x = np.linspace(-10, 10, 400)

    # Sigmoid
    sigmoid = tf.keras.activations.sigmoid
    plot_activation_function(sigmoid, x)

    # Tanh
    tanh = tf.keras.activations.tanh
    plot_activation_function(tanh, x)

    # ReLU
    relu = tf.keras.activations.relu
    plot_activation_function(relu, x)

    # Leaky ReLU
    leaky_relu = tf.keras.layers.LeakyReLU(alpha=0.1)
    plot_activation_function(leaky_relu, x)

    # ELU
    elu = tf.keras.layers.ELU(alpha=1.0)
    plot_activation_function(elu, x)

if __name__ == "__main__":
    main()
