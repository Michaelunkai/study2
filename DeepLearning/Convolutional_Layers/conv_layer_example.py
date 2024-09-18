import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # Define a convolutional layer
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size=3, stride=1, padding=1)
    
    def forward(self, x):
        # Apply convolutional layer and ReLU activation
        x = F.relu(self.conv1(x))
        return x

# Instantiate the model
model = SimpleCNN()
print(model)

# Create a dummy input tensor with shape [1, 1, 28, 28]
input_tensor = torch.randn(1, 1, 28, 28)

# Print the input tensor shape
print("Input shape:", input_tensor.shape)

# Pass the input tensor through the model
output_tensor = model(input_tensor)

# Print the output tensor shape
print("Output shape:", output_tensor.shape)
