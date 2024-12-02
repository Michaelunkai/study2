import numpy as np

# Generate a simple dataset
def generate_data():
    np.random.seed(1)
    X = np.random.randn(200, 2)  # 200 samples, 2 features
    y = np.array([1 if x0 * x1 > 0 else 0 for x0, x1 in X])
    y = y.reshape(-1, 1)
    return X, y

X, y = generate_data()

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialize weights and biases
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def sigmoid_derivative(self, z):
        return z * (1 - z)

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2

    def backward(self, X, y, output):
        self.output_error = y - output
        self.output_delta = self.output_error * self.sigmoid_derivative(output)

        self.z1_error = self.output_delta.dot(self.W2.T)
        self.z1_delta = self.z1_error * self.sigmoid_derivative(self.a1)

        self.W2 += self.a1.T.dot(self.output_delta)
        self.b2 += np.sum(self.output_delta, axis=0, keepdims=True)
        self.W1 += X.T.dot(self.z1_delta)
        self.b1 += np.sum(self.z1_delta, axis=0, keepdims=True)

    def train(self, X, y, epochs=1000):
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)

    def predict(self, X):
        output = self.forward(X)
        return np.round(output)

# Initialize the neural network
nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1)

# Train the neural network
nn.train(X, y)

# Make predictions
predictions = nn.predict(X)
accuracy = np.mean(predictions == y)
print(f'Accuracy: {accuracy * 100:.2f}%')
