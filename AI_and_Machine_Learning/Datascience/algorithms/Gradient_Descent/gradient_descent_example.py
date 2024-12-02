import numpy as np
import matplotlib.pyplot as plt

def compute_cost(X, y, theta):
    m = len(y)
    predictions = X.dot(theta)
    square_err = (predictions - y) ** 2
    return 1 / (2 * m) * np.sum(square_err)

def gradient_descent(X, y, theta, learning_rate, iterations):
    m = len(y)
    cost_history = np.zeros(iterations)
    theta_history = np.zeros((iterations, 2))

    for i in range(iterations):
        predictions = X.dot(theta)
        theta = theta - (1 / m) * learning_rate * (X.T.dot(predictions - y))
        theta_history[i, :] = theta.T
        cost_history[i] = compute_cost(X, y, theta)

    return theta, cost_history, theta_history

# Sample data
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

# Adding x0 = 1 to each instance
X_b = np.c_[np.ones((100, 1)), X]

# Setting hyperparameters
learning_rate = 0.1
iterations = 1000
theta = np.random.randn(2, 1)

theta, cost_history, theta_history = gradient_descent(X_b, y, theta, learning_rate, iterations)

# Plotting the cost function history
plt.plot(range(iterations), cost_history, 'b')
plt.xlabel("Number of iterations")
plt.ylabel("Cost (J)")
plt.title("Cost function history")
plt. ow()

print(f"Final parameters: {theta}")
