import numpy as np

# Generate a simple dataset
def generate_data():
    np.random.seed(1)
    X = np.random.randn(1000, 2)  # 1000 samples, 2 features
    y = np.array([1 if x0 * x1 > 0 else 0 for x0, x1 in X])
    y = y.reshape(-1, 1)
    return X, y

X, y = generate_data()

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01, regularization=0.01):
        # Initialize weights and biases
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2. / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2. / hidden_size)
        self.b2 = np.zeros((1, output_size))
        self.learning_rate = learning_rate
        self.regularization = regularization

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
        m = X.shape[0]
        
        # Compute gradients
        self.output_error = y - output
        self.output_delta = self.output_error * self.sigmoid_derivative(output)

        self.z1_error = self.output_delta.dot(self.W2.T)
        self.z1_delta = self.z1_error * self.sigmoid_derivative(self.a1)

        self.W2 += self.learning_rate * (self.a1.T.dot(self.output_delta) / m + self.regularization * self.W2)
        self.b2 += self.learning_rate * np.sum(self.output_delta, axis=0, keepdims=True) / m
        self.W1 += self.learning_rate * (X.T.dot(self.z1_delta) / m + self.regularization * self.W1)
        self.b1 += self.learning_rate * np.sum(self.z1_delta, axis=0, keepdims=True) / m

    def train(self, X, y, epochs=1000, batch_size=64):
        for epoch in range(epochs):
            permutation = np.random.permutation(X.shape[0])
            X_shuffled = X[permutation]
            y_shuffled = y[permutation]
            for i in range(0, X.shape[0], batch_size):
                X_batch = X_shuffled[i:i + batch_size]
                y_batch = y_shuffled[i:i + batch_size]
                output = self.forward(X_batch)
                self.backward(X_batch, y_batch, output)

    def predict(self, X):
        output = self.forward(X)
        return np.round(output)

# Initialize the neural network
nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1, learning_rate=0.01, regularization=0.01)

# Train the neural network
nn.train(X, y, epochs=1000, batch_size=64)

# Make predictions
predictions = nn.predict(X)
accuracy = np.mean(predictions == y)
print(f'Accuracy: {accuracy * 100:.2f}%')
