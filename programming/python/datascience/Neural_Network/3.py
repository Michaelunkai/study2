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
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01, regularization=0.01, dropout_rate=0.5):
        # Initialize weights and biases with He initialization
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2. / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2. / hidden_size)
        self.b2 = np.zeros((1, output_size))
        self.learning_rate = learning_rate
        self.regularization = regularization
        self.dropout_rate = dropout_rate

        # Initialize parameters for Adam optimizer
        self.mW1, self.mb1 = np.zeros_like(self.W1), np.zeros_like(self.b1)
        self.mW2, self.mb2 = np.zeros_like(self.W2), np.zeros_like(self.b2)
        self.vW1, self.vb1 = np.zeros_like(self.W1), np.zeros_like(self.b1)
        self.vW2, self.vb2 = np.zeros_like(self.W2), np.zeros_like(self.b2)
        self.beta1, self.beta2 = 0.9, 0.999
        self.epsilon = 1e-8
        self.t = 0

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def sigmoid_derivative(self, z):
        return z * (1 - z)

    def dropout(self, a):
        mask = np.random.binomial(1, 1 - self.dropout_rate, size=a.shape) / (1 - self.dropout_rate)
        return a * mask

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.a1 = self.dropout(self.a1)
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

        dW2 = self.a1.T.dot(self.output_delta) / m + self.regularization * self.W2
        db2 = np.sum(self.output_delta, axis=0, keepdims=True) / m
        dW1 = X.T.dot(self.z1_delta) / m + self.regularization * self.W1
        db1 = np.sum(self.z1_delta, axis=0, keepdims=True) / m

        # Adam optimizer
        self.t += 1
        self.mW1 = self.beta1 * self.mW1 + (1 - self.beta1) * dW1
        self.mb1 = self.beta1 * self.mb1 + (1 - self.beta1) * db1
        self.mW2 = self.beta1 * self.mW2 + (1 - self.beta1) * dW2
        self.mb2 = self.beta1 * self.mb2 + (1 - self.beta1) * db2

        self.vW1 = self.beta2 * self.vW1 + (1 - self.beta2) * (dW1 ** 2)
        self.vb1 = self.beta2 * self.vb1 + (1 - self.beta2) * (db1 ** 2)
        self.vW2 = self.beta2 * self.vW2 + (1 - self.beta2) * (dW2 ** 2)
        self.vb2 = self.beta2 * self.vb2 + (1 - self.beta2) * (db2 ** 2)

        mW1_hat = self.mW1 / (1 - self.beta1 ** self.t)
        mb1_hat = self.mb1 / (1 - self.beta1 ** self.t)
        mW2_hat = self.mW2 / (1 - self.beta1 ** self.t)
        mb2_hat = self.mb2 / (1 - self.beta1 ** self.t)

        vW1_hat = self.vW1 / (1 - self.beta2 ** self.t)
        vb1_hat = self.vb1 / (1 - self.beta2 ** self.t)
        vW2_hat = self.vW2 / (1 - self.beta2 ** self.t)
        vb2_hat = self.vb2 / (1 - self.beta2 ** self.t)

        self.W1 += self.learning_rate * mW1_hat / (np.sqrt(vW1_hat) + self.epsilon)
        self.b1 += self.learning_rate * mb1_hat / (np.sqrt(vb1_hat) + self.epsilon)
        self.W2 += self.learning_rate * mW2_hat / (np.sqrt(vW2_hat) + self.epsilon)
        self.b2 += self.learning_rate * mb2_hat / (np.sqrt(vb2_hat) + self.epsilon)

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
nn = NeuralNetwork(input_size=2, hidden_size=8, output_size=1, learning_rate=0.001, regularization=0.001, dropout_rate=0.5)

# Train the neural network
nn.train(X, y, epochs=2000, batch_size=32)

# Make predictions
predictions = nn.predict(X)
accuracy = np.mean(predictions == y)
print(f'Accuracy: {accuracy * 100:.2f}%')
